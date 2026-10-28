<script lang="ts">
	import StubPage from '$lib/StubPage.svelte';
	import { profileLinks } from '$lib/site';
</script>

<!-- Each profile link carries rel="me" so a profile that checks for a link
     back to this page can verify it. The list stays empty until each account
     exists. -->
<StubPage title="Links" description="Legalab profiles on other sites.">
	{#if profileLinks.length === 0}
		<p class="mt-6">This page is in development.</p>
	{:else}
		<ul class="mt-6 space-y-2">
			{#each profileLinks as link (link.href)}
				<li><a href={link.href} rel="me">{link.label}</a></li>
			{/each}
		</ul>
	{/if}
</StubPage>
