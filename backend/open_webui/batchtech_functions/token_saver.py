"""
title: Token Saver
author: BatchTechUI
version: 0.1.0
description: Cuts token spend. Asks for terse replies, resends only the latest messages, and shrinks old long messages and tool output.
"""

from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        priority: int = Field(0, description='Filter order (lower runs first)')
        terse: bool = Field(True, description='Add the terse-reply instruction to the system prompt')
        terse_prompt: str = Field(
            'Be terse. No preamble, no restating the question, no closing summary or offers. '
            'Short sentences, drop filler words. Code and exact commands stay complete.',
            description='Instruction added to the system prompt',
        )
        max_messages: int = Field(
            20, description='Resend at most this many recent non-system messages (0 = send everything)'
        )
        max_old_chars: int = Field(
            3000, description='Shrink older messages and tool output longer than this (0 = never shrink)'
        )

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: dict = None) -> dict:
        v = self.valves
        msgs = body.get('messages', [])
        system = [m for m in msgs if m.get('role') == 'system']
        rest = [m for m in msgs if m.get('role') != 'system']

        if v.max_messages and len(rest) > v.max_messages:
            rest = rest[-v.max_messages :]
            # Providers reject a history that starts on a tool or assistant turn.
            while rest and rest[0].get('role') != 'user':
                rest = rest[1:]

        if v.max_old_chars:
            for m in rest[:-1]:  # the latest message is always sent in full
                c = m.get('content')
                if isinstance(c, str) and len(c) > v.max_old_chars:
                    m['content'] = c[: v.max_old_chars] + '\n...[trimmed to save tokens]'

        if v.terse and v.terse_prompt.strip():
            if system:
                system[0]['content'] = (system[0].get('content') or '') + '\n\n' + v.terse_prompt
            else:
                system = [{'role': 'system', 'content': v.terse_prompt}]

        body['messages'] = system + rest
        return body
