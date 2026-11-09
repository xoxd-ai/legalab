<script lang="ts">
	// Shipping, v0 placeholder (TIN-7610). No shipping terms are decided, and
	// no Linear issue covers Legalab shipping yet (2026-11-08 go-live audit).
	//
	// Ruled so far: US only at launch (R-LEGALAB-20261031-b); own store first,
	// Reverb second (R-LEGALAB-20261031-a and -i). A shipping-included price was
	// proposed on TIN-7580 (comment d48885f5) and is not ruled.
	import StubPage from '$lib/StubPage.svelte';
	import DraftNotice from '$lib/DraftNotice.svelte';

	const decisions = [
		'Carrier and service level, and whether buyers can pick a faster one.',
		'Price: shipping included in the product price, a flat rate, or charged at checkout.',
		'Handling time: how many business days from order to the box leaving.',
		'Where we ship: US only is ruled; PO boxes, APO and FPO, Alaska, Hawaii and US territories are not.',
		'Box and packing: carton size and weight, inserts, and what ships in the same box.',
		'Insurance and signature on delivery, and above what order value.',
		'Tracking: who sends it and when.',
		'Lost or damaged in transit: who files the carrier claim, and what the buyer gets meanwhile.',
		'Wrong or undeliverable address: who pays to send it again.',
		'Sales tax on direct sales, which needs the state registration first.',
		'Shipping on Reverb orders, which Reverb sets on its side.',
		'Ship-from and return address on the label (the same question as the email postal address).',
	];
</script>

<StubPage title="Shipping" description="How Legalab ships. Not decided yet.">
	<DraftNotice open={['Every item in the list below.']} />

	<p class="mt-6">
		Nothing is for sale yet, and nothing about shipping is decided. When it is, this page will say
		what it costs, how long it takes and what happens if a box gets lost.
	</p>
	<p class="mt-4">Ruled so far: we ship to addresses in the United States only at launch.</p>

	<h2 class="mt-8 text-xl font-semibold">Decisions needed before this page can go public</h2>
	<ol class="mt-2 list-decimal space-y-1 pl-6">
		{#each decisions as item (item)}
			<li>{item}</li>
		{/each}
	</ol>
</StubPage>
