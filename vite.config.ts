import { sveltekit } from '@sveltejs/kit/vite';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import tailwindcss from '@tailwindcss/vite';
import { accessibilityPlugin } from '@tummycrypt/vite-plugin-a11y';
import { skeletonColorUtilities } from '@tummycrypt/vite-plugin-skeleton-colors';
import { escapeSvelte, mdsvex } from 'mdsvex';
import { codeToHtml } from 'shiki';
import type { PreprocessorGroup } from 'svelte/compiler';
import { defineConfig } from 'vite';
import adapter from './kit.adapter.js';

// Code-surface contract (the glorious.build pattern): svx code fences are
// highlighted AT BUILD TIME by shiki with a light and dark theme pair and
// `defaultColor: false`, so the emitted `pre.shiki` markup carries only
// `--shiki-light` / `--shiki-dark` custom properties per token; src/app.css
// walks those variables into painted colour, keyed on data-mode. No shiki
// byte ever reaches the client bundle: this runs inside the mdsvex
// preprocessor, and the output is static HTML.
const SHIKI_THEMES = { light: 'github-light', dark: 'github-dark' };

async function highlighter(code: string, lang: string | null | undefined) {
	const html = await codeToHtml(code, {
		lang: lang || 'text',
		themes: SHIKI_THEMES,
		defaultColor: false,
	});
	return `{@html \`${escapeSvelte(html)}\`}`;
}

const mdsvexPreprocessor = mdsvex({ extensions: ['.svx'], highlight: { highlighter } }) as PreprocessorGroup;

// mdsvex 0.12.x still emits the legacy Svelte module-script spelling for
// frontmatter. Rewrite it at preprocess time so the public log remains
// build-time content under runes mode.
const mdsvexSvelte5Preprocessor: PreprocessorGroup = {
	...mdsvexPreprocessor,
	async markup(options) {
		const result = await mdsvexPreprocessor.markup?.(options);
		if (!result?.code) return result;
		return {
			...result,
			code: result.code.replaceAll('<script context="module">', '<script module>'),
		};
	},
};

export default defineConfig({
	optimizeDeps: { exclude: ['@xoxd/public-chrome'] },
	server: { watch: { ignored: ['**/bazel-*', '**/bazel-*/**'] } },
	plugins: [
		skeletonColorUtilities(),
		tailwindcss(),
		accessibilityPlugin({ wcagLevel: 'AA', failOnError: false }),
		// SvelteKit 3 reads its configuration from the sveltekit() plugin;
		// svelte.config.js is no longer supported. The adapter is kit.adapter.js.
		sveltekit({
			extensions: ['.svelte', '.svx'],
			preprocess: [vitePreprocess(), mdsvexSvelte5Preprocessor],
			compilerOptions: {
				runes: true,
				// Remote functions (RU3) need Svelte's async mode.
				experimental: { async: true },
			},
			// RU3: SvelteKit remote functions are the estate pattern. Still
			// behind the experimental flag in Kit 3.0.x.
			experimental: { remoteFunctions: true },
			adapter,
			paths: {
				// GitHub Pages project-path hosting needs base="/<repo>" (set BASE_PATH in CI);
				// a custom domain / Cloudflare uses base="".
				base: (process.env.BASE_PATH ?? '') as '' | `/${string}`,
			},
			prerender: {
				handleHttpError: 'warn',
				handleMissingId: 'warn',
				handleUnseenRoutes: 'warn',
			},
		}),
	],
});
