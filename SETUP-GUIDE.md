# Set up Paperclip CLN, Ark and Wallet on Start9

A short LAN setup guide for the **Sideflash test packages on StartOS 0.4, x86-64**. These builds are experimental and unaudited. Start with small amounts and keep full backups.

**Setup order:** Bitcoin node → CLN → Ark Server → Wallet.

## 1. Install the packages and prepare your node

Download the Sideflash prerelease `.s9pk` files from the release pages and sideload them through StartOS:

- [Paperclip CLN](https://github.com/connorslab/paperclip-cln-startos/releases)
- [Paperclip Ark Server](https://github.com/connorslab/paperclip-asp-startos/releases)
- [Paperclip Wallet](https://github.com/connorslab/paperclip-wallet-startos/releases)

Use compatible Sideflash releases; Ark needs the automatic-registration update (rc.6 or later). Have a synced XBT Bitcoin node, its RPC URL, username and password ready. Use the node's reachable LAN IP and actual RPC port, such as `http://NODE_LAN_IP:RPC_PORT`. Allow RPC access from StartOS over your private network. An internal Docker hostname from another device will not work.

## 2. Set up CLN

Open **Configure test app** in Paperclip CLN:

1. Enter the node RPC connection and a recognizable node alias.
2. Set the TLS hostname to the stable hostname clients will use, without a port. Choose it before first startup; changing it later requires credential migration.
3. Start CLN and enable its **CLN gRPC** and **Hold gRPC** interfaces. Use the external ports assigned by StartOS, not the container ports.
4. Open **Connect Ark server**, check both HTTPS URLs, and copy the **Private connection bundle**. It contains spending-capable credentials; keep it private.
5. Use the included RTL interface to manage peers and channels. Lightning sending needs outbound liquidity; receiving needs inbound liquidity. Installing the app does not fund it or open channels.

## 3. Set up Ark Server

1. Open **Configure test app**, enter the node RPC details, and supply an on-chain recovery sweep address you control.
2. Enable the **pruned-node adapter** if the backend is pruned. Leave **automatic registration** enabled for simpler Sideflash testing.
3. Save the settings and access token. With Ark stopped, use **Import CLN connection** to paste the bundle from CLN, then start Ark.
4. Open **Operator interface**, unlock with the token, and initialize only if this is a fresh server. Recover an existing instance from its backup instead.
5. Wait for indexing to synchronize. Use **Funding balances** to inspect the server's funding information. Ark payout/pool funding, recovery reserves and CLN channel liquidity are separate; funding one does not fund the others. Depositing can trigger pool issuance and on-chain fees.

If the CLN hostname cannot resolve, set **CLN connection IP (optional)** to its host's LAN IP. Keep the original HTTPS hostname in the connection URLs so certificate verification still works.

## 4. Set up Wallet

1. Copy **Ark endpoint** from the Ark app's Interfaces, including its assigned external port. Use this client endpoint, not the operator webpage. The LAN Ark endpoint uses raw HTTP/2 (`http://HOST:PORT`).
2. In Wallet's **Configure test app**, set the Ark server URL. For a pruned backend, enable the adapter and enter the node RPC settings. Save the access token and start Wallet.
3. Open **Wallet interface**, unlock, and create a new wallet. The Ark URL should already be filled from StartOS settings. Changing that setting does not migrate an existing wallet or its funds.
4. Complete the node connection setup. With the adapter enabled, wait for indexing and use **Connection details and funding information** to obtain its internal connection credentials for onboarding. That internal URL is only for this wallet. Otherwise use your node's reachable RPC connection.
5. Save the complete recovery backup and verify the intended Ark server identity.

## 5. Test a small payment

Under **Send & receive**, generate an Ark or Sideflash address. The wallet automatically creates a reusable Lightning offer if none exists. With Ark automatic registration enabled, no manual recipient allowlist is needed.

Check the payment estimate, send a small test amount, and verify the recipient balance. Keep the apps running for new Lightning/Sideflash requests and automatic refreshes; closing the browser does not stop the wallet daemon. Test Sideflash addresses expire after at most 24 hours, so generate a fresh address when necessary.

## Quick troubleshooting

| Symptom | Check |
| --- | --- |
| RPC hostname cannot resolve | Use a reachable LAN IP and the correct RPC port. |
| RPC returns 403 | Check the node's RPC access restrictions for the StartOS connection. |
| Lightning relay offline / connection refused | CLN running, both interfaces enabled, assigned external ports, imported credentials, and hostname resolution. |
| Sideflash registration disabled | Use an Ark package with automatic registration support and enable the setting. |
| Lightning configured but payment fails | Channel direction/capacity, Ark pool inventory, sync status, and payment estimate. Configured does not mean funded. |

**Backups:** stop each app before its StartOS backup and include all volumes. Never run an original and restored instance of the same identity together, and never restore stale Lightning state over a live node. A seed alone is not a complete backup of this stack.
