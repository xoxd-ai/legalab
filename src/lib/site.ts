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
	{ href: '/about', label: 'About' },
	{ href: '/links', label: 'Links' },
];

export const footerSections = [
	{ heading: 'Site', links: navLinks },
	{
		heading: 'Policies',
		links: [
			{ href: '/privacy', label: 'Privacy' },
			{ href: '/terms', label: 'Terms' },
		],
	},
];

// Profiles rendered on /links with rel="me". Add one only after the account
// exists and links back to this site.
export const profileLinks: SiteLink[] = [];
