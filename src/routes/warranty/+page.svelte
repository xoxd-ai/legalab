<script lang="ts">
	// Written limited warranty, v0 draft (TIN-7610, TIN-7626). Not in force.
	//
	// Evidence and limits:
	// - Term: operator ruling R-LEGALAB-20261031-c, quoted on TIN-7580 comment
	//   b62dfdee: "1-year limited, 30-day returns (Recommended)". The ruling says
	//   the wording is a draft only (legal boundary TIN-2345).
	// - Form: BIZ-22, "A written limited warranty with clear terms, plus a
	//   separate, non-contractual ... pledge". No "full" or "lifetime" wording
	//   (claims gate check FullOrLifetimeWarranty, TIN-7607).
	// - Signer: BIZ-24, a named human signs warranties. Seller line: R-LEGALAB-
	//   20261031-a, "Legalab by xoxd.ai". Legal home: BIZ-44, the xoxd.ai LLC
	//   once filed, until then a d/b/a.
	// - Region: US only at launch, R-LEGALAB-20261031-b.
	// - Exclusions start from the go-live checklist draft, worded generically:
	//   nothing public from the hardware lane (R-LEGALAB-20261028-a, naming
	//   hold TIN-7598).
	// - Reverb is Legalab's own second channel (R-LEGALAB-20261031-i), so
	//   whether those sales count as "from us" is bracketed, here and on the
	//   returns page.
	// - Options B and C (connected gear, consequential damages) and the used
	//   exclusion, which depends on section 7, are bracketed for legal review.
	// - The disclosure lines (warrantor, coverage, remedy, how to claim, the
	//   state-law sentences) follow the Magnuson-Moss written warranty rules as
	//   remembered (15 U.S.C. 2301 ff., 16 CFR 701 and 702). Unverified here:
	//   legal review confirms each line before the page goes public.
	import StubPage from '$lib/StubPage.svelte';
	import DraftNotice from '$lib/DraftNotice.svelte';

	const open = [
		'Legal review of every clause (TIN-2345 or its successor).',
		'Warrantor: the legal name and postal address that give this warranty.',
		'Signer: the named person who signs it, and the date.',
		'Start date: purchase date or delivery date.',
		'Remedy: repair or replace only, or also refund.',
		'Who pays shipping for a warranty claim, each way.',
		'Whether the warranty passes to a second owner, which decides the used-product exclusion.',
		"Whether sales on Legalab's own Reverb listings count as bought from us.",
		'Whether to keep options A, B and C below (implied warranties, other gear, consequential damages).',
		'Support contact: no support mailbox exists yet.',
		'Which products it covers once each one has a public name.',
	];
</script>

<StubPage title="Limited Warranty" description="The Legalab one-year limited warranty. Draft, not in force.">
	<DraftNotice {open} />

	<p class="mt-6">
		This is the written limited warranty for Legalab hardware. Read it before you buy. If you want
		the plain-talk version of how we treat people, that is on the
		<a href="/pledge">We stand behind it</a> page, which is a separate promise and not part of
		this warranty.
	</p>

	<h2 class="mt-8 text-xl font-semibold">1. Who gives this warranty</h2>
	<p class="mt-2">
		[WARRANTOR: legal name and postal address], selling as Legalab by xoxd.ai ("we").
	</p>

	<h2 class="mt-8 text-xl font-semibold">2. What it covers</h2>
	<p class="mt-2">
		Legalab hardware bought new from us [REVERB: including / not including sales on Legalab's own
		Reverb listings] and shipped to an address in the United States. We
		warrant it against defects in materials and workmanship under normal use.
	</p>
	<p class="mt-2">Covered products: [PRODUCT LIST: added as each product is named].</p>

	<h2 class="mt-8 text-xl font-semibold">3. How long it lasts</h2>
	<p class="mt-2">One (1) year from [the date of purchase / the date of delivery].</p>

	<h2 class="mt-8 text-xl font-semibold">4. What we will do</h2>
	<p class="mt-2">
		If a covered defect shows up within that year, we will repair the product or replace it
		[or refund the price you paid], at our choice, with no charge for parts or labor. A repaired
		or replacement product is covered for the rest of the original year.
	</p>

	<h2 class="mt-8 text-xl font-semibold">5. What it does not cover</h2>
	<ul class="mt-2 list-disc pl-6">
		<li>Damage caused by a power supply or accessory other than one we supplied.</li>
		<li>Damage caused by modification or repair by someone other than us.</li>
		<li>Damage from accidents, drops, liquid, fire, misuse, or use against the instructions.</li>
		<li>Normal wear, scratches and other cosmetic marks that do not affect how it works.</li>
		<li>[OPTION B, legal review: Other gear used with the product.]</li>
		<li>
			[IF SECTION 7 IS THE ORIGINAL BUYER ONLY: Products bought used.] Products bought from anyone
			other than us [or an authorized seller].
		</li>
	</ul>

	<h2 class="mt-8 text-xl font-semibold">6. How to make a claim</h2>
	<p class="mt-2">
		Email [SUPPORT ADDRESS] within the warranty period with your order number and a short
		description of the problem. We will reply with instructions. Shipping for a claim is paid by
		[us / you / us one way].
	</p>

	<h2 class="mt-8 text-xl font-semibold">7. Who is covered</h2>
	<p class="mt-2">[The original buyer only / The original buyer and any later owner].</p>

	<h2 class="mt-8 text-xl font-semibold">8. Implied warranties</h2>
	<p class="mt-2">
		[OPTION A, legal review: Any implied warranty of merchantability or fitness for a particular
		purpose is limited to the one-year term of this written warranty. Some states do not allow
		limits on how long an implied warranty lasts, so this limit may not apply to you.]
	</p>

	<h2 class="mt-8 text-xl font-semibold">9. Incidental and consequential damages</h2>
	<p class="mt-2">
		[OPTION C, legal review: We are not responsible for incidental or consequential damages, such
		as lost gigs, lost recording time or damage to other equipment. Some states do not allow the
		exclusion or limitation of incidental or consequential damages, so this exclusion may not
		apply to you.]
	</p>

	<h2 class="mt-8 text-xl font-semibold">10. Your rights under state law</h2>
	<p class="mt-2">
		This warranty gives you specific legal rights, and you may also have other rights which vary
		from state to state.
	</p>

	<p class="mt-8">Signed: [NAME], for Legalab by xoxd.ai. Date: [DATE].</p>
</StubPage>
