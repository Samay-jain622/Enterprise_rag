from deepteam import Guardrails
from deepteam.guardrails import (
    PromptInjectionGuard,
    TopicalGuard,
    PrivacyGuard,
    ToxicityGuard,
)

guardrails = Guardrails(
    input_guards=[
        PromptInjectionGuard(),
        PrivacyGuard(),
        ToxicityGuard(),
        TopicalGuard(
            allowed_topics=[
                "kubernetes",
                "pods",
                "deployments",
                "services",
                "ingress",
                "helm",
                "kubectl",
                "rbac",
                "configmaps",
                "secrets",
            ]
        )
    ],output_guards=[]
)


