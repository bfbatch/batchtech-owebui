<script lang="ts">
	// BATCHTECH: label that rotates through a user-configurable word list while a model is working.
	import { onDestroy, onMount } from 'svelte';
	import { settings } from '$lib/stores';

	const DEFAULT_THINKING_WORDS = [
		'Thinking',
		'Pondering',
		'Cogitating',
		'Percolating',
		'Noodling',
		'Simmering',
		'Ruminating',
		'Musing',
		'Contemplating',
		'Mulling',
		'Brewing',
		'Churning',
		'Deliberating',
		'Spelunking',
		'Marinating',
		'Synthesizing',
		'Cerebrating',
		'Wrangling'
	];

	$: thinkingWords = (() => {
		const custom = ($settings?.thinkingWords ?? '')
			.split(/[\n,]/)
			.map((w) => w.trim())
			.filter(Boolean);
		return custom.length > 0 ? custom : DEFAULT_THINKING_WORDS;
	})();

	let index = Math.floor(Math.random() * 1000);
	let timer: ReturnType<typeof setInterval> | null = null;

	onMount(() => {
		timer = setInterval(() => (index += 1), 2000);
	});
	onDestroy(() => {
		if (timer) clearInterval(timer);
	});
</script>

{thinkingWords[index % thinkingWords.length]}...
