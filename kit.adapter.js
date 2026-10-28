// SvelteKit adapter selection, kept in its own module so the adapter is one
// reviewed file rather than a block inside vite.config.ts. SvelteKit 3 reads
// its configuration from the `sveltekit()` Vite plugin (svelte.config.js is
// no longer supported); vite.config.ts imports this default export.
//
// Static default (adapter-static). A site that needs a server (remote
// `query`/`form`/`command`) swaps in `@sveltejs/adapter-node` here.
import adapter from '@sveltejs/adapter-static';

export default adapter({
	pages: process.env.BUILD_OUTPUT_DIR ?? 'build',
	assets: process.env.BUILD_OUTPUT_DIR ?? 'build',
	fallback: '404.html',
	precompress: true,
	strict: false,
});
