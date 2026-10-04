import { setupManifest } from '@start9labs/start-sdk'
import { long, short } from './i18n'
export const manifest = setupManifest({
  id: 'paperclip-ark-sideflash', title: 'Paperclip Ark Sideflash', license: 'MIT',
  packageRepo: 'https://github.com/connorslab/paperclip-asp-startos',
  upstreamRepo: 'https://github.com/connorslab/paperclip-asp',
  marketingUrl: 'https://ark.paperclippool.xyz', donationUrl: null,
  description: {short, long}, volumes: ["main", "startos", "asp", "config", "postgres"],
  images: {"app": {"source": {"dockerTag": "paperclip-ark-startos:sideflash-20261004-1"}, "arch": ["x86_64"]}, "postgres": {"source": {"dockerTag": "postgres:17-bookworm"}, "arch": ["x86_64"]}}, dependencies: {},
})
