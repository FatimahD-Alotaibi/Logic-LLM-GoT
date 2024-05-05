# Logic-LLM-GoT

<p align="center">
  <img src="symbolic_formulator_with_got.png">
</p>

This implementation converts a natural language logical reasoning problem into symbolic logic using a formulator. The prompt undergoes transformation into a symbolic logic representation of the original question, which is then processed through a framework of thought graphs.

## Logic Program Generation

To generate logic programs for logical reasoning problems in each dataset, at the root directory, run the following commands:

```bash
cd ./logic_llm_got
python models/logic_program.py \
    --api_key "Your OpenAI API Key" \
    --dataset_name "Dataset Name [ProntoQA | ProofWriter | FOLIO | LogicalDeduction ｜ AR-LSAT]" \
    --split dev \
    --model_name "Model Name [text-davinci-003 | gpt-4]" \
    --max_new_tokens 1024 \
```

The generated logic programs will be saved in `outputs/logic_programs`. You can also reuse the logic programs we generated in `./outputs/logic_programs`.
