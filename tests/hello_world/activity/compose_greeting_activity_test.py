from unittest import TestCase

from hello_world.activity.compose_greeting_activity import ComposeGreetingInput, compose_greeting


class ComposeGreetingTest(TestCase):
    async def test_return_greeting(self):
        result = await compose_greeting(greeting_input=ComposeGreetingInput('hello', 'folks'))
        self.assertEquals('hello folks', result)
