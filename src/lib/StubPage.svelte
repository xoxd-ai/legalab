<script lang="ts">
	import type { Snippet } from 'svelte';

	let { title, description, children }: { title: string; description: string; children?: Snippet } =
		$props();
</script>

<svelte:head>
	<title>{title === 'Legalab' ? title : `${title} | Legalab`}</title>
	<meta name="description" content={description} />
</svelte:head>

<main class="page-shell">
	<h1>{title}</h1>
	{@render children?.()}
</main>
