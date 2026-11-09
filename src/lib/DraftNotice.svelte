<script lang="ts">
	// Draft banner for v0 pages (TIN-7610). Every page that carries it is a
	// draft: nothing on it is in force, and the open list names what the
	// operator still has to decide before the page can go public.
	let { open = [] }: { open?: string[] } = $props();
</script>

<aside class="draft-notice mt-6 rounded border-2 border-dashed p-4" aria-label="Draft notice">
	<p class="font-semibold">Draft. Not in force. Not published.</p>
	<p class="mt-2">
		This page is a working draft for review. Nothing on it is an offer, a promise or a policy
		yet. Text in square brackets is a placeholder for a decision that has not been made.
	</p>
	{#if open.length > 0}
		<p class="mt-2 font-semibold">Open before this page can go public:</p>
		<ul class="mt-1 list-disc pl-6">
			{#each open as item (item)}
				<li>{item}</li>
			{/each}
		</ul>
	{/if}
</aside>
