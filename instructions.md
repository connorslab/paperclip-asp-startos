# Paperclip Ark Server Sideflash test

This is a separate **experimental, unaudited test app** for StartOS 0.4, x86-64 only. It does not upgrade an existing production app. It creates no channels, transfers no money, and copies no existing wallet data during installation. Runtime tests are not a StartOS device installation test.

Keep the entire app backup. Stop the app before a backup; the package refuses an active-state backup. Restore only with the original instance stopped. Never run both restored and original copies of the same Lightning or Ark identity. Never restore an old Lightning state over a live node.

## Documentation

- [Sideflash integration](https://github.com/connorslab/paperclip-asp/blob/feature/sideflash/docs/sideflash.md)

## What this app provides

Bitcoin Ark server, watchman, private PostgreSQL database, and optional pruned-node adapter. Reusable BOLT12 and Sideflash receive support are enabled when a CLN connection is configured.

Operator UI: 3000 (bearer token). Ark client gRPC: 3535. PostgreSQL 5432, admin RPC 3536, watchman admin RPC, and adapter 18336 remain internal. The Ark endpoint is a raw HTTP/2 connection on the LAN, not an HTTPS web page.

## Setup

1. Configure and start the separate CLN app first. Use **Connect Ark server** to copy its private connection bundle.
2. Run **Configure test app** using the labeled fields (JSON below is reference only). Supply your private XBT node RPC settings and an on-chain `sweep_address` you control for recovery. Save the backend settings, then use **Import CLN connection** to paste the exported bundle. Leave automatic registration enabled; no recipient keys are needed. Save the returned operator access token.
3. For a pruned backend, set `pruned` to `true`. The bundled adapter indexes locally and the ASP waits for it to synchronize. Historical blocks must still be retrievable from the network; this is not instant archival recovery. Full indexed nodes may use `false`.
4. Start the app, open **Operator interface**, enter the access token, and initialize a **new** ASP only if this is a fresh instance. Initialization creates new keys and database state. Restore backups instead when recovering an existing server.
5. Point the test wallet to **Ark endpoint**. Create its fresh wallet and open Sideflash receiving. With automatic registration enabled, the ASP verifies the wallet and acknowledges its address without manual recipient approval.
6. Run **Funding balances** to inspect funding information. Funding, recovery reserve, CLN channels and receiving inventory are separate requirements. No initial funding is included. Review balances before making any deposit.

The test configuration permits Lightning amounts up to 50,000 sats, targets two 50,000-sat pool outputs and retains a 20,000-sat on-chain pool refill reserve. Funding the server can trigger configured pool issuance and on-chain fees. These are lab defaults, not a production liquidity policy. Recipient fees and recovery allocations still apply.

```json
{
  "network": "bitcoin",
  "rpc_url": "http://NODE_LAN_IP:8332",
  "rpc_user": "RPC_USERNAME",
  "rpc_password": "RPC_PASSWORD",
  "pruned": false,
  "recipient_allowlist": [],
  "cln": null,
  "sweep_address": "YOUR_OWN_ONCHAIN_RECOVERY_ADDRESS"
}
```

## Backup and access

Stop the app, then use StartOS Backup. Back up all volumes, not only a seed. **Configure test app** can rotate the web access token while stopped. Client TLS credentials are independent of that token. Package signing keys are not wallet keys.

## Validation limits

See VALIDATION.md in the feature branch. These files have not been installed on a StartOS device by the builder. No mainnet funds are included. Start with tiny, disposable test amounts only after verifying connectivity, backup/restore and identity.

## Labeled configuration form

Configure test app now loads saved settings into separate fields. JSON examples above are reference only. Passwords and client private keys are masked. For Wallet, node RPC fields are only required when the pruned-node adapter is enabled; otherwise enter RPC settings during wallet onboarding. For Ark, enable Lightning and paste each certificate/key and endpoint into its matching field. Recipient public keys may be comma- or space-separated. Token rotation remains optional.

## One-copy CLN connection (rc.4)

In the running CLN app, open **Connect Ark server**. Matching enabled gRPC URLs are prefilled; otherwise copy the CLN and Hold HTTPS URLs from Interfaces. Run the action and copy the entire **Private connection bundle**. It contains spending-capable credentials: keep it private.

Configure the Ark backend first, stop Ark, then open **Import CLN connection** and paste the bundle. This fills both endpoints and all three TLS credentials, enables Lightning, and preserves the other settings and tokens. Start Ark afterward. Importing validates the bundle but does not prove network reachability; your LAN/DNS and enabled interfaces still need to work.

No individual certificate fields need copying. Export does not generate a funding address or move funds.

The operator dashboard reports Lightning as configured or disabled from the running service state. Configured is not a payment-readiness check: verify CLN connectivity, channel capacity and Ark pool liquidity.

## Automatic Sideflash registration (rc.6)

Automatic registration is enabled by default in this test package. Wallets no longer need manual recipient approval. The ASP still verifies recipient signatures, its server/chain binding, an active wallet-owned BOLT12 offer, request size and expiry. Disable automatic registration to require the recipient list again. This does not enable public networking or move funds.

If Ark cannot resolve your CLN hostname, set **CLN connection IP (optional)** to the CLN host LAN IP. Keep the original HTTPS hostname in both URLs so certificate checks remain valid. This mapping is reapplied at startup; update it if the host IP changes. Use the IP of your own CLN host.
