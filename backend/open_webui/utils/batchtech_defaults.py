# BATCHTECH: install built-in functions once, on startup.
import logging
from pathlib import Path

from open_webui.models.functions import FunctionForm, FunctionMeta, Functions
from open_webui.models.users import Users

log = logging.getLogger(__name__)

FUNCTIONS_DIR = Path(__file__).resolve().parent.parent / 'batchtech_functions'

# id, name, description, file. Installed enabled and global, only if the id does not exist yet,
# so an admin can disable, edit or delete them and a restart never brings them back or overwrites edits.
DEFAULT_FUNCTIONS = [
    (
        'token_saver',
        'Token Saver',
        'Terse replies, trims old history and tool output to cut token spend.',
        'token_saver.py',
    ),
]


async def install_batchtech_functions():
    admin = await Users.get_super_admin_user()
    if not admin:
        log.info('BatchTechUI: no admin yet, built-in functions install on the next start')
        return
    for fid, name, description, filename in DEFAULT_FUNCTIONS:
        try:
            if await Functions.get_function_by_id(fid):
                continue
            content = (FUNCTIONS_DIR / filename).read_text()
            form = FunctionForm(id=fid, name=name, content=content, meta=FunctionMeta(description=description))
            await Functions.insert_new_function(admin.id, 'filter', form)
            await Functions.update_function_by_id(fid, {'is_active': True, 'is_global': True})
            log.info(f'BatchTechUI: installed built-in function {fid}')
        except Exception as e:
            log.exception(f'BatchTechUI: could not install built-in function {fid}: {e}')
