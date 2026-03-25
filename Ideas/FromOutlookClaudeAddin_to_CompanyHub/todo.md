# 1. Continue early phase brainstorming 

## email is just one part of the whole tool (just the starting point)
   - the product name shall not be related to mail

## mail indexing
  - some mailboxes include thousands of mails
  - how to index them (as separate agent, not block the major agent/s)
  - goal: lookeen replacement and AI supported search
  - goal: central vector DB, usable by all users
  - goal: private vector DB, usable by individual users (e.g. for private mailbox)
  - goal: configure, which mailboxes to continuously update the index (or parts of mailboxes)

## solution shall run on Linux/MAC-OS (at least the parts that are not bound to Windows)
  
## The tool shall provide deterministic workflows that run with priority over AI workflows
   - only use AI, if it is needed (or if configured)
   - no automatic AI handling for critical parts
     - AI: alwaysAsk by default or yolo mode, if configured
     - Examples
       - moving mails 
       - deleting mails (AI: alwaysAsk or yolo mode)
       - ...

## architecture and other basic topics
    - I have asked 3 AIs about this: The prompt was as follows:
            I am starting a large project from scratch that shall be created via ai agents. Multiple techniques will be used (e.g. outlook plugins, webapp, maybe browser plugins, python, C#, typescript, javascript). I want to keep a stable and maintainable architecture, human as well as ai readable and maintainable solution that can be enhanced starting from a small POC (outlook plugin) up to a AI driven company helper agent. Are there open source or commervial tools that can support here. I think of potential agent middleware software, architecture templates, coding conventions, code and architecture review approaches etc.
    - see the different results in
      C:\PROJ\OutlookClaudeAddin\brainstorming\AI_Agent_Architecture_Guide*.md
    - does using openclaw provide any benefits to consider it as part of the architecture
        - whole repo: C:\PROJ\openclaw, documentation in the doc subfolder
        - pros and cons of using openclaw 
        - risk!
        - create new nodes/plugins to openclaw for security reasons
        - any role for step 1 (outlook plugin), or comes into the game later?
    - compare using the different platforms and middlewares 
      - pro/con table
      - what can be combined, what is mutually exclusive
    - which coding conventions to use, how to apply them
      - some ideas can be found in C:\PROJ\acontis-ai\Coding\CodingConventions
        this needs to be expanded and consolidated before coding starts
    - codereview: how to assure architecture goals and coding conventions are fulfilled
    - test driven development
      - before starting a coding session, a clear, unambiguos and fully testable success goal must be defined. The AI agent shall run fully autonoumosly until coding, review and testing has finished
      - unit tests shall assure that if new features are added, the old ones shall still work
  
  ## potential step by step approach, or just define step 1 and keep flexible
  
  ## which languages to use for which use case?
    - python? (venv!): great AI support, but version difficulties
    - typescript, javascript
    - C#

@@@ hier weiter
# 2. critical review of the whole brainstorming result
  only after phase 1 is finished

  