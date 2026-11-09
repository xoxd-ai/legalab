<script lang="ts">
	// "We stand behind it" pledge, v0 draft (TIN-7610, TIN-7626). Not a contract.
	//
	// Evidence and limits:
	// - BIZ-22: a separate, non-contractual "we support every product we sell"
	//   pledge in the brand voice, beside the written limited warranty.
	// - R-LEGALAB-20261109-c (TIN-7580 comment 3692423c): the earlier rulings
	//   stand over the 2026-11-08 brief, so there is no support-until-2069 line
	//   and no "we replace it" promise here.
	// - BIZ-23: clean copy, no profanity. Brand voice: punk and clean.
	// - No repair, recycling or durability claim: none is backed in the
	//   claims register yet (TIN-7607).
	import StubPage from '$lib/StubPage.svelte';
	import DraftNotice from '$lib/DraftNotice.svelte';

	const open = [
		'Approval of the wording and the voice.',
		'Whether to offer paid repairs after the warranty year, and how to say it.',
		'Support contact: no support mailbox exists yet.',
	];
</script>

<StubPage title="We stand behind it" description="How Legalab treats the people who buy its gear. Not a contract.">
	<DraftNotice {open} />

	<p class="mt-6 font-semibold">
		This page is a pledge, not a contract. It does not add to or change the written
		<a href="/warranty">limited warranty</a>, which is the only warranty we give.
	</p>

	<h2 class="mt-8 text-2xl font-semibold">We support every product we sell.</h2>

	<p class="mt-4">
		We build gear for bands splitting gas money four ways and holding their rig together with tape
		and stubbornness. We know what it costs you when something quits
		on a Friday. So here is how we try to act.
	</p>

	<ul class="mt-4 list-disc space-y-2 pl-6">
		<li>
			<span class="font-semibold">Ask us anything.</span> Before you buy, after you buy, when you
			are wiring something odd at 2 a.m. You get a straight answer, and we say so when the answer is
			"we do not know yet".
		</li>
		<li>
			<span class="font-semibold">We tell you what is proven.</span> When we say a number, we say
			where it came from: measured, or only simulated. If it has not been measured, we
			say that.
		</li>
		<li>
			<span class="font-semibold">Tell us first.</span> If something we made stops working, tell
			us first. We will help you work out what is wrong.
		</li>
		<li>
			<span class="font-semibold">No runaround.</span> We will not hide behind fine print we did
			not show you. The warranty is short and on its own page, so you can read it before you buy.
		</li>
	</ul>

	<p class="mt-6">Reach us at [SUPPORT ADDRESS].</p>
</StubPage>
