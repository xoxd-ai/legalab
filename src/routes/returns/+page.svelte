<script lang="ts">
	// Returns, v0 draft (TIN-7610). Not in force.
	//
	// Evidence and limits:
	// - The 30-day window is the only returns term on record: operator ruling
	//   R-LEGALAB-20261031-c, quoted on TIN-7580 comment b62dfdee as
	//   "1-year limited, 30-day returns (Recommended)", with the note that the
	//   wording is a draft only (legal boundary TIN-2345). The ruling sets no
	//   start date, condition, shipping, refund or fee terms, so each of those is
	//   a bracketed placeholder for the operator.
	// - Region: US only at launch, R-LEGALAB-20261031-b.
	// - Channels: own store first, Reverb second (R-LEGALAB-20261031-a and -i).
	//   Reverb is Legalab's own second channel, so whether a Reverb sale counts
	//   as "from us" is bracketed, matching the warranty page. Reverb runs its
	//   own returns setting (7-day default, read by the 2026-11-08 go-live
	//   audit), so a Reverb policy needs its own ruling.
	// - Arrived broken is a shipping matter, not a warranty claim: the warranty
	//   excludes accidents and drops. It points at the shipping lost-or-damaged
	//   decision, which is open.
	import StubPage from '$lib/StubPage.svelte';
	import DraftNotice from '$lib/DraftNotice.svelte';

	const open = [
		'Legal review of the wording (TIN-2345 or its successor).',
		'Start of the 30 days: purchase date or delivery date.',
		'Condition: unused only, or used and working; original box required or not.',
		'Who pays return shipping when nothing is wrong with the product.',
		'Refund method and how fast it is sent; whether original shipping is refunded.',
		'Restocking fee: none, or how much.',
		"Whether sales on Legalab's own Reverb listings count as bought from us.",
		'The returns setting for any Reverb listing, which Reverb handles on its side.',
		'What a buyer does when the box arrives damaged (the shipping lost-or-damaged decision).',
		'Support contact and return address: neither exists yet.',
	];
</script>

<StubPage title="Returns" description="The Legalab 30-day returns policy. Draft, not in force.">
	<DraftNotice {open} />

	<p class="mt-6 text-lg">Changed your mind? You have 30 days.</p>

	<h2 class="mt-8 text-xl font-semibold">The window</h2>
	<p class="mt-2">
		You can return Legalab hardware bought from us within 30 days of [the date of purchase / the
		date of delivery].
	</p>

	<h2 class="mt-8 text-xl font-semibold">What we need back</h2>
	<p class="mt-2">
		[CONDITION: for example, the product and everything else that came in the box, in working
		order; original box required or not].
	</p>

	<h2 class="mt-8 text-xl font-semibold">How to start a return</h2>
	<p class="mt-2">
		Email [SUPPORT ADDRESS] with your order number before you send anything. We will reply with the
		return address and what to put in the box.
	</p>

	<h2 class="mt-8 text-xl font-semibold">Shipping and refunds</h2>
	<ul class="mt-2 list-disc pl-6">
		<li>Return shipping is paid by [you / us].</li>
		<li>
			Once the return arrives and we have checked it, we refund [the price paid / the price paid
			and the original shipping] to [the original payment method] within [N] days.
		</li>
		<li>Restocking fee: [none / amount].</li>
	</ul>

	<h2 class="mt-8 text-xl font-semibold">If it arrived broken</h2>
	<p class="mt-2">
		[LOST OR DAMAGED IN SHIPPING: what to do and what you get, not decided yet; see the
		<a href="/shipping">shipping</a> page].
	</p>

	<h2 class="mt-8 text-xl font-semibold">If it stopped working</h2>
	<p class="mt-2">
		That is a warranty claim, not a change-of-mind return. See the
		<a href="/warranty">limited warranty</a>.
	</p>

	<h2 class="mt-8 text-xl font-semibold">Bought on Reverb</h2>
	<p class="mt-2">
		[REVERB: a purchase from Legalab's own Reverb listing counts as bought from us under this
		policy / follows that listing's Reverb returns setting: REVERB RETURNS SETTING].
	</p>
</StubPage>
