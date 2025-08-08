from langchain.tools import StructuredTool  # to handle multiple arguments
from pydantic.v1 import BaseModel


def write_report(filename, html):
    with open(filename, "w") as f:  # open up file in write mode and call it f
        f.write(html)

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

# just remember use structured to recieve multiple arguments
write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema,
)
