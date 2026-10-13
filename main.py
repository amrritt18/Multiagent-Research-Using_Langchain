
from src.pipeline.pipeline import run_research_pipeline

result = run_research_pipeline(
    "Recent applications of multi-agent AI systems"
)

print("\nFinal report:")
print(result["report"])

print("\nCritic feedback:")
print(result["feedback"])
