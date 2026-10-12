# M0-07 bootstrap quarantine inspection

> **Version/date:** 0.1 / 2026-10-12 Asia/Jakarta
> **Status:** PARTIAL ACQUISITION; LOCAL EXECUTION / INSTALLATION NOT AUTHORIZED.
> **Trace:** M0-07, FR-PLT-001, NFR-MAINT-001; no successor task started.

## 1. Genuine authority and preserved bindings

The owner answered **“Terima paket; izinkan karantina saja”** to the EV-0068 review packet on local commit `d6e690cf2316d0a035de4e24b182ec90ee5fe662`. This accepts that exact artifact set for bounded acquisition/static inspection only. It does not authorize executing acquired code, installation, SDK/target/provider requests, remote CI, provisioning, upload or push. The original packet/JSON retain their historical PROPOSED/PENDING labels and exact reviewed bytes; this dated record supplies the later narrow decision without rewriting them.

| Reviewed file | SHA-256, still unchanged |
|---|---|
| [Bootstrap review](BOOTSTRAP_REVIEW.md) | `0FD2FF58734792E151EF00C4D67B9D91D84B268CFCAF78F727DBBB4509BC2CC0` |
| [Exact artifact manifest](bootstrap-artifacts.json) | `8FEDFF4BE21ABAC355B8B9251D55608F75C7E2864BB6E7676C53C00CF32DEEFE` |
| [Completion roadmap](IMPLEMENTATION_PLAN.md) | `08BFD0627EC00AE7C22B56AAEE016282F94E2DE2BA7381FC31AD0F217D5826D3` |

Allowed repository edits in this increment are this report and corresponding todo.md tracking only. Local artifacts/receipts reside in `D:/Dev/PACT/.bootstrap/quarantine/EV-0068-d6e690c/`; local `.git/info/exclude` excludes that directory. Existing source, tests, accepted foundation documents and the two preexisting untracked documents are preserved. Acquired executables were never extracted, imported, installed or run.

## 2. Actual outcome and limits

**35/36 complete files:** all 30 wheels and 5/6 CPython archives have the exact reviewed SHA-256 and length. Complete bytes: **291,653,309**. One Windows CPython 3.14.8 archive is incomplete: **16,777,216** of **23,228,299** bytes, partial SHA-256 `A7798C14AAD6B0F6B9C47F269093C6B588D10A095269336F81CE90DC2C3B08BF`. A partial hash is evidence of the fragment, never verification of the intended artifact. It was not parsed as an archive.

The first download process ceased before its final receipt was saved; a later session poll returned unknown process ID. Its final exit status and exact transfer/duration counters are unavailable. File timestamps place initial writes around 01:33 Jakarta; when interruption was investigated around 05:22, the original 30-minute acquisition window had elapsed. **No recovery HTTP request or automatic retry occurred.** Offline inspection was reconstructed from retained bytes. A preliminary recovery command exited before making requests because the time-window guard rejected it.

Persisted artifact bytes, including the fragment, are **308,430,525**. A conservative artifact-payload allowance of three in-flight 1-MiB buffers yields **311,576,253 bytes**, below the approved 1-GiB cap; this is an estimate of the interrupted attempt, not a measured final network counter. HTTP/TLS overhead is not measured. Current quarantine storage including text receipts is **312,428,181 bytes**, below 2 GiB. Paid-service cost zero; no purchased service was invoked. Do not report successful completion within the wall-time budget, complete transport telemetry, or verified matrix execution.

The downloader accepted only exact reviewed HTTPS URLs, checked allowed hosts/ports, rejected userinfo/query destinations outside approved GitHub asset CDNs, used no proxy/auth credentials, limited redirects to three, concurrency to three and retries to zero. Body reads had length/hash, transfer and monotonic time guards. Signed redirect URLs were never logged. Redirect-host histories from the interrupted process were not retained, so this report does not invent per-file redirect receipts. Guards and bytes provide bounded acquisition evidence; they do not prove absence of all other machine network activity.

### 2.1 Per-artifact results

For VERIFIED rows, the SHA-256 below is the actual full-file digest and equals the reviewed expected digest. Manifest retains exact approved source URL, matrix mapping and publisher size. No replacement artifact/version was selected.

| File | Actual bytes | Acquisition / static inspection | Actual SHA-256 |
|---|---:|---|---|
| `uv-0.13.0-py3-none-win_amd64.whl` | 15,819,247 | VERIFIED / static checks pass | `0367B4E0AE4DCEF32DA4AA2AD2F3853B6AD81D50C187ABE50D343D892B8FEA21` |
| `uv-0.13.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | 17,941,073 | VERIFIED / static checks pass | `52C7DA0FD9056D9551124777EC77DE53F0DF7017DAF8F98A19E947B7837416ED` |
| `hatchling-1.32.4-py3-none-any.whl` | 78,748 | VERIFIED / static checks pass | `08ECF7548FB48205E7F213D70C71E67B8271B7242093DC3F1DA578B42C734A2C` |
| `pytest-9.1.1-py3-none-any.whl` | 386,536 | VERIFIED / static checks pass | `37A86B45EFB9A47A61A36449063E8E18D0CAB3161329FC099EB21783169C4F0C` |
| `ruff-0.16.8-py3-none-win_amd64.whl` | 10,586,899 | VERIFIED / static checks pass | `A6B85621FD3C81E31FC5F5ADD09C9C078B430DB3595CA632EFAFDEC9E64EBFAA` |
| `ruff-0.16.8-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | 10,323,796 | VERIFIED / static checks pass | `15E7D226246961DB9235098333CAA13063906D3851136B84C2900B82F5DAA1DF` |
| `mypy-2.4.0-cp312-cp312-win_amd64.whl` | 11,381,574 | VERIFIED / static checks pass | `236E0D68F6941992B0811128E652590F590DB444AB29AD8F1324765B9298B946` |
| `mypy-2.4.0-cp313-cp313-win_amd64.whl` | 11,389,803 | VERIFIED / static checks pass | `295ECF2E57542CD836CA537486951289678C8C7D1EE6AD74EBE29B2168A003CF` |
| `mypy-2.4.0-cp314-cp314-win_amd64.whl` | 11,576,345 | VERIFIED / static checks pass | `2106B55105BA5EA9BE4F53A24517FC5FA927FF1585EDC9BC1A975ABB72CAEF89` |
| `mypy-2.4.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 15,552,257 | VERIFIED / static checks pass | `29EB0B9427A6B11B992E452F6CCEB8AF724F4DCEB47E779D0B35E405E996EA5E` |
| `mypy-2.4.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 15,465,557 | VERIFIED / static checks pass | `6BE721BD4BD57576193653B75B4AF3461C9D0BF7DD8B528F782E9BE210DC75BB` |
| `mypy-2.4.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 15,441,463 | VERIFIED / static checks pass | `20E9A5CD875837520C43DB98DEA0B6D0C2197833D95C30127D8F570FB9B1F00B` |
| `packaging-26.3-py3-none-any.whl` | 129,956 | VERIFIED / static checks pass | `D7193F7C8E4E93F444FDE0262BF90AF30E16FA0AD0AD44CB553C87339B23CD1C` |
| `pathspec-1.1.1-py3-none-any.whl` | 57,328 | VERIFIED / static checks pass | `A00CE642F577BF7F473932318056212BC4F8BFDF53128C78BBD5AF0B9B20B189` |
| `pluggy-1.6.0-py3-none-any.whl` | 20,538 | VERIFIED / static checks pass | `E920276DD6813095E9377C0BC5566D94C932C33B27A3E3945D8389C374DD4746` |
| `trove_classifiers-2026.9.21.13-py3-none-any.whl` | 14,232 | VERIFIED / static checks pass | `8B1FF4F9C191B1040B71C37F1E445AB99732911E3CD91DE52838453A854D7A17` |
| `iniconfig-2.3.1-py3-none-any.whl` | 7,552 | VERIFIED / static checks pass | `9121E2C1FDB355232495BE3194C8DFE87CCC2D5DEE45947B78E68F499790D7A7` |
| `pygments-2.21.0-py3-none-any.whl` | 1,250,147 | VERIFIED / static checks pass | `2363C69B61C4A97C838DA3B130DCD6468F4848992B21A82F2A63EC34377137D9` |
| `colorama-0.4.6-py2.py3-none-any.whl` | 25,335 | VERIFIED / static checks pass | `4F1D9991F5ACC0CA119F9D443620B77F9D6B33703E51011C16BAF57AFB285FC6` |
| `mypy_extensions-1.1.0-py3-none-any.whl` | 4,963 | VERIFIED / static checks pass | `1BE4CCCDB0F2482337C4743E60421DE3A356CD97508ABADD57D47403E94F5505` |
| `typing_extensions-4.16.0-py3-none-any.whl` | 45,571 | VERIFIED / static checks pass | `481CAA481374E813C1B176ADA14E97F1F67A4539CE9CFEB3F350D78D6370C2E8` |
| `librt-0.16.0-cp312-cp312-win_amd64.whl` | 126,176 | VERIFIED / static checks pass | `25A58A19EA8D83B68209F04912DF765E9260635EF77646542ED4B4ABE6BC7940` |
| `librt-0.16.0-cp313-cp313-win_amd64.whl` | 126,180 | VERIFIED / static checks pass | `14ED6EBE3E4F85F326D7920011AD30FF49ED9334E62CF88CAEF9BA973D9E3A92` |
| `librt-0.16.0-cp314-cp314-win_amd64.whl` | 120,464 | VERIFIED / static checks pass | `3F0B8114C44B2AC06FF5DACD08E07E8E807FF4F46083F2A1602685122559BE41` |
| `librt-0.16.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 531,952 | VERIFIED / static checks pass | `36E53948E99BBE3FFEA257124CFCAE1CFB01831555C9A9C903C9F9A72DB7FD07` |
| `librt-0.16.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 531,689 | VERIFIED / static checks pass | `17BAC7F7A16B328FFF77E440287693EB017ABDE913595B5827EBCCBC21ECD8A6` |
| `librt-0.16.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` | 523,057 | VERIFIED / static checks pass | `CA8052401C55D7511DDA6760719FDA7618067E83535D7D0010096D216C34B667` |
| `tomlkit-0.15.1-py3-none-any.whl` | 49,449 | VERIFIED / static checks pass | `177A05AECE5A8CA5266FD3C448ABB47B8D352F09D477D3CA8332DB4D89B24304` |
| `ast_serialize-0.12.1-cp39-abi3-win_amd64.whl` | 1,165,798 | VERIFIED / static checks pass | `3D6ED63D4FC1EC867B8CB522D58C36DF0E8F05E487BEA0FFD102043A37636D72` |
| `ast_serialize-0.12.1-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` | 1,311,809 | VERIFIED / static checks pass | `50A9EAEDF1DB4857DAD7CC47DD757ED70BFCC40B89D44D516C4A2F0D5033BD76` |
| `cpython-3.12.15+20261009-x86_64-pc-windows-msvc-install_only_stripped.tar.gz` | 22,011,208 | VERIFIED / static checks pass | `11ED9F8A6AC64FB1B5A55E40E305A6744A3F77A70863C8F8197A6E4349ABC64A` |
| `cpython-3.12.15+20261009-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz` | 34,304,557 | VERIFIED / static checks pass | `FFA8F85F1B56E88B687F08D743D817015524B86A9365FD921243132B80F1A36D` |
| `cpython-3.13.16+20261009-x86_64-pc-windows-msvc-install_only_stripped.tar.gz` | 21,969,508 | VERIFIED / static checks pass | `3A7ADFB69E3FF02A41ED38AC637808532B438AB3C8619AF46CA5DBEC5C1F5190` |
| `cpython-3.13.16+20261009-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz` | 35,082,735 | VERIFIED / static checks pass | `24801EA31C7D406D559A17E2226325C723D50C56900B9C0DA7B62ADAAE2AFFC9` |
| `cpython-3.14.8+20261009-x86_64-pc-windows-msvc-install_only_stripped.tar.gz` | 16,777,216 | INTERRUPTED / NOT RUN | `A7798C14AAD6B0F6B9C47F269093C6B588D10A095269336F81CE90DC2C3B08BF` |
| `cpython-3.14.8+20261009-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz` | 36,299,807 | VERIFIED / static checks pass | `DDC902FD26460F728758C67D80417C1031EDF97589F1F162C4BA3AA158A35998` |

## 3. Static checks and adverse cases

All 30 wheels were read as ZIP data only. Identity, version, Requires-Python, no-extra Requires-Dist, WHEEL text and every payload RECORD SHA-256/length were checked. ZIP CRC validation occurs while reading; absolute/traversal/drive/backslash/NUL paths, duplicates, unsupported link/type entries and excessive expansion are rejected. Bounds: 100,000 members, 128 MiB per entry, 1 GiB expanded size per archive, 2 MiB per notice text read. These are inspector bounds, not accepted runner limits.

Initial literal metadata comparison failed for Hatchling/pathspec/Pygments because wheel markers used different quotes or whitespace. Reinspection normalized only that syntax, kept whitespace within literals and used no eval. Actual dependency identities/specifiers/markers still match the reviewed set. Colorama/mypy-extensions had no declared-license list in the review metadata; the initial checker incorrectly iterated null. It was corrected to represent absent metadata and inspect actual notice files. The initial interrupted process had no final exit result; later reconstructed failure results are retained separately.

The three Linux archives initially failed a Windows-style case-fold collision check. Full inventory identified exactly 25 distinct terminfo case pairs in each, e.g. `2621A`/`2621a`. Reinspection correctly checks Linux as case-sensitive while preserving exact duplicate rejection; **do not extract these Linux archives onto a Windows case-insensitive filesystem**. All five complete archives passed bounded name/type/expansion checks. Linux relative symlinks/hardlinks stay within the archive's `python/` root and resolve through finite chains to inventoried members; cycles, escaping, absolute and unresolved links fail. No archive extraction occurred.

Offline inspector adverse checks: **15/15 expected rejections/distinctions**, six malicious paths, six unsafe URL structures/destinations, and three changed dependency version/extra/marker cases. Formatting equivalence and literal-space distinction also pass. These test the local analysis guard, not PACT's future executor or sandbox. No claim of arbitrary malware detection, trusted publisher attestation or full supply-chain audit is made.

## 4. License/notice observations and remaining gaps

Every inspected wheel contains its primary license text; all declared paths that were present in review metadata were found. Colorama's actual `licenses/LICENSE.txt` and mypy-extensions' `licenses/LICENSE` are present despite absent declared lists. pathspec's wheel contains MPL-2.0 text. This confirms the reviewed license observation, not a new publication-license decision. Retain these texts in any later local installation or authorized distribution.

| Component | Actual notice evidence | Remaining verification |
|---|---|---|
| uv, both wheels | LICENSE-APACHE and LICENSE-MIT; same hashes across platforms | No complete native dependency/license bill of materials present as a dedicated wheel file; map bundled components to pinned build inputs before closing bundle review |
| Ruff, both wheels | Composite LICENSE, 20,731 bytes; SHA-256 `2597D854122B77DDC71971564CA2350A37608575CE324ADC5650A2B2051C8F18` | Composite text observed; match native build/component inventory, do not describe top-level MIT alone as full bundle clearance |
| mypy / librt | Combined license text plus mypy typeshed/LICENSE, including MIT/PSF/ISC/Apache notice sections | Platform-specific notice hashes recorded; preserve texts and map selected native/vendor components |
| ast-serialize | LICENSE plus crates/LICENSE in both wheels | Composite crates notice present; exact native component mapping still pending |
| pathspec | MPL-2.0 LICENSE; SHA-256 `FAB3DD6BDAB226F1C08630B1DD917E11FCB4EC5E1E020E2C16F83A0A13863E85` | Local development only; no modified dependency or publication/distribution authorized |
| Remaining Python tool wheels | Primary license/notice text and hashes inventoried | No resolver/build/runtime validation yet |
| Five complete CPython archives | CPython LICENSE.txt and pip 26.2.1/vendor notices are bundled; 45 notice files per Windows archive and 43 per Linux archive | `PYTHON.json` is absent in stripped archives. CPython LICENSE alone does not establish license mapping for every linked native library; reconcile exact build composition and additional notices before execution proposal |
| Windows CPython 3.14.8 | Fragment only | Full acquisition/hash/archive/notice inspection NOT RUN |

Notice detection examined bounded LICENSE/COPYING/NOTICE/COPYRIGHT/AUTHORS text and archive names. It is not exhaustive semantic classification of arbitrary embedded notice strings or binary linkage. License text is preserved in local receipts with path/size/hash; this report avoids reproducing full third-party licenses. The acquisition-only acceptance is not inferred as acceptance of unreviewed component risks.

### 4.1 Local evidence bindings

- `inspection-receipt.json` SHA-256: `26ECD859F11EC972AAA4CE329CA5F53EB98AC7B98349652E2286AEA3E92C6784`; ignored local quarantine record, no secrets/signed redirect URLs. The first reconstructed receipt retains 32 static passes and three Linux-check failures; the final record contains 35 static passes, one interrupted file and 15 adverse checks.
- `inspection-final.json` SHA-256: `F8F663201DDC8EDEBBD8957A6141545DF3369C95006E2531472B1F715744055C`; ignored local quarantine record, no secrets/signed redirect URLs. The first reconstructed receipt retains 32 static passes and three Linux-check failures; the final record contains 35 static passes, one interrupted file and 15 adverse checks.

## 5. Commands and exact limitations

All analysis used the preexisting `C:/Program Files/Python314/python.exe` 3.14.4 with `-X utf8 -I -B`. Scripts were locally authored in `C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/`, never imported from acquired payloads.

| Exact command / action | Actual result |
|---|---|
| `& 'C:/Program Files/Python314/python.exe' -X utf8 -I -B 'C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/acquire_inspect.py'` | Interrupted process; final exit unavailable; 35 complete files + one 16-MiB fragment retained. Initial metadata/null-list failures reported; no receipt or completed-in-budget claim |
| `& 'C:/Program Files/Python314/python.exe' -X utf8 -I -B 'C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/recover_inspect.py'` — initial invocation | Exit 1 at expired-window assertion before any HTTP request |
| Same recovery command, revised to offline inspection only | Exit 1: 35 full hashes/lengths match, 32 static passes, three Linux case-check failures, one interrupted file; reconstructed receipt retained |
| `& 'C:/Program Files/Python314/python.exe' -X utf8 -I -B 'C:/Users/user/AppData/Local/Temp/PACT-bootstrap-20261012/finalize_inspect.py'` | Exit 1 deliberately reflects incomplete 36-file acquisition: 35 full hash/length/static passes, one interrupted/NOT RUN; 15 adverse checks meet expectations; Linux check correction explained above |
| Existing interpreter stdin diagnostics for wheel Requires-Dist and tar notice/path inventories | Exit 0; quote/space differences, absent declarations, 25 terminfo case pairs/archive and notice paths inspected without extraction/import |

`git diff --check`, staged whitespace, evidence preservation and ledger/digest checks are recorded in todo EV-0069 with their actual outcomes before the local checkpoint commit. Source/unit/lint/mypy/pytest/project build/lock/clean-install checks **NOT RUN**: no workspace/tool install exists or is authorized. Acquired uv/Python/any package execution, six-cell runtime matrix, CI, OS containment, human approval, targets/providers/hosted/corpus/external tool checks **NOT RUN**. No GitHub push or service activation occurred.

## 6. Unblock path and decisions

M0-07 remains **BLOCKED**, not DONE. Its architecture DoD still requires clean checkout installation from lock, smoke locally and in actual CI, side-effect-free import and no committed .env secrets. Static bytes are not any of those runtime outcomes.

1. A **new bounded time window** is needed only to finish the interrupted exact Windows Python 3.14.8 artifact. Proposed recovery: one fresh GET to its unchanged EV-0068 URL/hash, preserve the old fragment, transfer cap 64 MiB, additional storage cap 64 MiB, wall time 10 minutes, zero paid cost, same HTTPS/CDN allowlist/max-three redirects/no automatic retry. Static inspection only; no install/execution. This is renewal after expiry, not reopening the accepted artifact/design choices. Stop on failure, changed size/hash or budget.
2. Continue safe primary-source/build metadata and notice reconciliation for bundled native components; no new binary or package acquired under the original permission. Propose any additional provenance artifact acquisition concretely if needed.
3. Only after findings are resolved, present the exact local execution/install scope: verified artifacts into project-local isolated tools/runtimes/venv; offline/no-index/no-source-build fallback, reviewed build/runtime hashes, pins/lock, bounded checks and cleanup. Do not run an acquired tool to discover its behavior while approval is pending. Remote source upload/CI remains a separate decision.

Already accepted tooling/DSL/threat/fixture/ID/job/audit directions and disabled-profile choices are unchanged. No owner decision is requested again for them. No task after M0-07 has started.
