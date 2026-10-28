import { FOUC_SCRIPT } from '@xoxd/public-chrome/fouc';
import type { Handle } from '@sveltejs/kit/hooks';
export const handle: Handle = async ({ event, resolve }) => resolve(event, { transformPageChunk: ({ html }) => html.replace('</head>', `<script>${FOUC_SCRIPT.replace(/<\/script/gi, '<\\/script')}</script></head>`) });
