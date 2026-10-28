<script lang="ts">
	import { page } from '$app/state';
	import { PublicNavigation, SiteFooter } from '@xoxd/public-chrome';
	import '../app.css';
	import { site, navLinks, footerSections } from '$lib/site';

	let { children } = $props();
	const identity = { name: site.name, homeHref: '/' };
</script>

<div class="flex min-h-screen flex-col">
	<a href="#content" class="sr-only focus:not-sr-only">Skip to content</a>
	<PublicNavigation {identity} pathname={page.url.pathname} {navLinks} quickLinks={navLinks} />
	<div id="content" class="flex-1">{@render children?.()}</div>
	<SiteFooter {identity} tagline={site.tagline} sections={footerSections} />
</div>
