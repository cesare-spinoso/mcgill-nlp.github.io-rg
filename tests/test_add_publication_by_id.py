import unittest
from textwrap import dedent

import src.python.add_publication_by_id as mod

expected_content = """---
author: Siva Reddy
categories: Publications
link: https://arxiv.org/abs/2004.09456
names: Moin Nadeem, Anna Bethke, Siva Reddy
tags:
- ACL
title: 'StereoSet: Measuring stereotypical bias in pretrained language models'
venue: ACL 2020

---

*{{ page.names }}*

**{{ page.venue }}**

{% include display-publication-links.html pub=page%}

## Abstract

A stereotype is an over-generalized belief about a particular group of people, e.g., Asians are good at math or African Americans are athletic. Such beliefs (biases) are known to hurt target groups. Since pretrained language models are trained on large real-world data, they are known to capture stereotypical biases. It is important to quantify to what extent these biases are present in them. Although this is a rapidly growing area of research, existing literature lacks in two important aspects: 1) they mainly evaluate bias of pretrained language models on a small set of artificial sentences, even though these models are trained on natural data 2) current evaluations focus on measuring bias without considering the language modeling ability of a model, which could lead to misleading trust on a model even if it is a poor language model. We address both these problems. We present StereoSet, a large-scale natural English dataset to measure stereotypical biases in four domains: gender, profession, race, and religion. We contrast both stereotypical bias and language modeling ability of popular models like BERT, GPT-2, RoBERTa, and XLnet. We show that these models exhibit strong stereotypical biases. Our data and code are available at https://stereoset.mit.edu."""


class TestAddPublicationById(unittest.TestCase):
    def test_add_publication_by_id(self):
        issue_body = dedent(
            """
            ### Method

            DOI

            ### Identifier

            10.18653/v1/2021.acl-long.416

            ### Month

            08

            ### Day

            01    
        """
        )
        parsed = mod.parse_issue_body(issue_body)
        paper_json = mod.fetch_content(parsed)
        paper_json = mod.wrangle_fetched_content(parsed, paper_json)  # in-place
        formatted = mod.format_parsed_content(paper_json)
        mod.write_content_to_file(formatted)

        with open("_posts/papers/2020-08-01-2004.09456.md", "r") as f:
            content = f.read()

        self.assertEqual(content, expected_content)


if __name__ == "__main__":
    unittest.main()
