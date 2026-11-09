// Site identity and navigation. Copy here is stub copy: it makes no product,
// performance or safety claim. Product pages and claims wait for the claims
// register (TIN-7607) and the pinned claims sync (TIN-7659).

export interface SiteLink {
	href: string;
	label: string;
}

export const site = {
	name: 'Legalab',
	tagline: 'This site is in development.',
	description: 'The Legalab website. This site is in development.',
} as const;

export const navLinks: SiteLink[] = [
	{ href: '/', label: 'Home' },
	{ href: '/waitlist', label: 'Waitlist' },
	{ href: '/about', label: 'About' },
	{ href: '/links', label: 'Links' },
];

// The warranty, pledge, returns and shipping pages are v0 drafts (TIN-7610).
// Each one carries a DraftNotice and states no policy in force.
export const footerSections = [
	{ heading: 'Site', links: navLinks },
	{
		heading: 'Policies',
		links: [
			{ href: '/warranty', label: 'Limited warranty' },
			{ href: '/pledge', label: 'We stand behind it' },
			{ href: '/returns', label: 'Returns' },
			{ href: '/shipping', label: 'Shipping' },
			{ href: '/privacy', label: 'Privacy' },
			{ href: '/terms', label: 'Terms' },
		],
	},
];

// Profiles rendered on /links with rel="me". Add one only after the account
// exists and links back to this site.
export const profileLinks: SiteLink[] = [];
