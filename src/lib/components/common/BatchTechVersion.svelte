<script lang="ts">
	// BATCHTECH: shows BatchTechUI's own version, with the BatchTechUI version it is based on.
	import { getContext } from 'svelte';
	import { WEBUI_BUILD_HASH, WEBUI_VERSION } from '$lib/constants';
	import { WEBUI_NAME, config } from '$lib/stores';
	import Tooltip from './Tooltip.svelte';

	const i18n: any = getContext('i18n');

	// Only a real commit hash (passed as --build-arg BUILD_HASH=...) is shown.
	$: hash = /^[a-f\d]{7,64}$/i.test(WEBUI_BUILD_HASH ?? '') ? WEBUI_BUILD_HASH.slice(0, 7) : '';
</script>

<Tooltip content={WEBUI_BUILD_HASH}>
	<span>
		{#if $config?.batchtech_version}
			{$WEBUI_NAME} v{$config.batchtech_version}{#if hash}
				· {hash}{/if}
			<span class="text-gray-400 dark:text-gray-500"
				>({$i18n.t('based on Open WebUI')} v{WEBUI_VERSION})</span
			>
		{:else}
			v{WEBUI_VERSION}
		{/if}
	</span>
</Tooltip>
