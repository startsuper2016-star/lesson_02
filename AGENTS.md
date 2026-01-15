# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: Bash("openskills read <skill-name>")
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>weekly-report</name>
<description>专业周报生成与优化技能，支持从零创建周报、改进现有周报、提供周报模板。适用于:(1)用户提供工作内容需要生成结构化周报 (2)用户已有周报草稿需要优化改进 (3)用户需要周报模板或写作指导。支持自由文本和结构化混合输入模式，输出简洁要点式周报，包含本周工作完成情况、下周工作计划、问题与风险三部分结构。</description>
<location>global</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
