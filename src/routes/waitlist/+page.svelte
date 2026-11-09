<script lang="ts">
	// Waitlist stub, v0 draft (TIN-7610, TIN-7624). The form has no action and
	// no backend: its fieldset is disabled, nothing is sent and nothing is
	// stored. Signup opens only after the operator rules on the open items below.
	//
	// Evidence and limits:
	// - No product name, product claim, form factor or build status: nothing
	//   public from the hardware lane (R-LEGALAB-20261028-a), and public use of
	//   the first product's name waits on the naming review (TIN-7598,
	//   TIN-7624 Q1).
	// - CAN-SPAM: every commercial email needs a valid physical postal address
	//   and a working opt-out. The postal address waits on the PO box
	//   (TIN-7591). Requirement text is from memory of 15 U.S.C. 7704 and
	//   16 CFR 316, unverified here; legal review confirms it.
	// - Open and bracketed in the copy: double opt-in (TIN-7672), the opt-out
	//   method, one-click or other (TIN-7674), and what one opt-out stops
	//   (SPR-101).
	// - Copy rules: R-LEGALAB-20261109-c (BIZ-22, BIZ-23 stand).
	import StubPage from '$lib/StubPage.svelte';
	import DraftNotice from '$lib/DraftNotice.svelte';

	const open = [
		'Postal address for the email footer: the PO box is not rented yet.',
		'Form backend and the opt-out route: none is connected.',
		'Whether signup needs a confirmation click (double opt-in).',
		'The opt-out method, and what leaving the list stops.',
		'Privacy notice: what is collected, why, how long it is kept, who can see it.',
		'Form fields: the content bank has a field list that still needs a ruling.',
		'Whether the page may name the first product before the naming review.',
	];
</script>

<StubPage title="Waitlist" description="Get on the Legalab list. Signup is not open yet.">
	<DraftNotice {open} />

	<p class="mt-6 text-lg">
		Gear for bands who load their own van, play the basement show and still want their rig to
		sound right.
	</p>
	<p class="mt-4">
		Legalab is a small shop for metal and punk players on a shoestring budget. Nothing is for sale
		yet. When something is, the list hears first.
	</p>

	<h2 class="mt-8 text-xl font-semibold">Signup is not open yet</h2>
	<p class="mt-2">
		This form is a placeholder. It is switched off, it has nowhere to send anything, and nothing
		you type here leaves your browser.
	</p>

	<form class="mt-4" onsubmit={(event) => event.preventDefault()} aria-describedby="waitlist-closed">
		<fieldset disabled class="space-y-4">
			<legend id="waitlist-closed" class="font-semibold">Waitlist signup (closed)</legend>
			<label class="block">
				<span class="block">Email</span>
				<input type="email" name="email" autocomplete="email" class="mt-1 w-full max-w-md rounded border p-2" />
			</label>
			<label class="block">
				<span class="block">Band or project (optional)</span>
				<input type="text" name="band" class="mt-1 w-full max-w-md rounded border p-2" />
			</label>
			<button type="submit" class="rounded border px-4 py-2">Signup opens soon</button>
		</fieldset>
	</form>

	<h2 class="mt-8 text-xl font-semibold">What the list will get</h2>
	<ul class="mt-2 list-disc pl-6">
		<li>A note when there is something to order, and news along the way.</li>
		<li>
			[DOUBLE OPT-IN, open: a confirmation email first, and you are not on the list until you
			click it / no confirmation step].
		</li>
		<li>
			Every email carries our postal address [POSTAL ADDRESS: waits on the PO box] and a way off
			the list [OPT-OUT METHOD, open: one click / another method].
		</li>
		<li>
			Leaving the list stops [OPT-OUT SCOPE, open: every email from us / email from this list
			only]. See the privacy notice [PRIVACY NOTICE: not written yet].
		</li>
	</ul>
</StubPage>
