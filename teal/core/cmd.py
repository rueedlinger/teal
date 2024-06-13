import asyncio


class AsyncSubprocess:
    def __init__(self, cmd, tmp_dir):
        self.cmd = cmd
        self.tmp_dir = tmp_dir

    async def run(self):
        process = await asyncio.create_subprocess_shell(
            self.cmd,
            env={"HOME": self.tmp_dir},
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        return Result(process.returncode, stdout, stderr)


class Result:
    def __init__(self, returncode, stdout, stderr):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return f"returncode: {self.returncode}, stdout: {self.stdout}, stderr: {self.stderr}"
