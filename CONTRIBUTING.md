# Contributing

Start from the existing operating-model intake. Identify the decision owner, affected blueprint and a concrete failure case. Reuse the canonical upstream implementation wherever it has an owner. Include a pinned revision, license, exact verification commands, observed outcome and limits for every new binding.

Open a draft PR with an anonymized or synthetic fixture, its expected receipt and one negative case. Run `python3 -m unittest discover -s tests`. For changes that alter authority, data boundaries, skills or routing, request a review from the relevant owner and an independent reviewer. Human reviewers check the quality of the decision and teaching transfer as well as code correctness.

Submit only material you can license under the terms in LICENSE. Keep private conversations, customer records, unreleased creative assets, personal workspaces and credentials in their owning environment.
