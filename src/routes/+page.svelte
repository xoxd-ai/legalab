<script lang="ts">
	import StubPage from '$lib/StubPage.svelte';
	import { site } from '$lib/site';
</script>

<StubPage title={site.name} description={site.description}>
	<p class="mt-6">This site is in development. Pages will appear here as they are ready.</p>
</StubPage>
