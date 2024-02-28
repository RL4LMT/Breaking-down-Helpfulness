# Notes

## Meeting with Polina 15.02

**Reseach questions:**
- What helpfullness really is? 
- Does it coincide with our componentwise annotation?
- Which categories (components) are most important?
- How components correlate to the catgeories?
- Own idea?
  
**Annotation:**
- Actually less than 25% of the dataset
- Pick 3 categories
- Find a subset of 3-4 least arguable commponents (through 50 items & per-task inter-annotator agreement)
1) Is the answer generally helpful? -> 1/0 
2) Is the component (length, info, etc.) relevant? -> 1/0
  - If yes -> does the answer satisfy  the aspect?-> 1/0 


**LLM Experiments**:
- CHhoose a pretrained LLM that preferably was not trained on our dataset and was was fine-tuned with RLHF
- Generate answers with a pretrained LLM of our choise (100)
- Check these responses in respect of helpfulness in general and single components
- Analyze the performance of the model in comparison to humans, e.g.  is the model as bad us humans?
- Only inference for data creation
  
**Result:**
- ACL style paper (up to 8 pages)
- This repo with documneted code
- Annotated dataset

## Meeting with Polina 15.02

**Grice's Maxims:**
- good idea, but difficult to evaluate them in practise
- hardly applicable for any catgeories except QA 
- we can assume that all maxims are relevant in conversational setting

