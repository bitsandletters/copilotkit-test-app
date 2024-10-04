"use client";

import * as React from 'react'
import { useCoAgent, useCopilotChat } from "@copilotkit/react-core";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";

interface WeatherAgentState {
  final_response: {
    temperature: number;
    wind_direction: string;
    wind_speed: number;
    conditions: string;
  },
  input: string,
  messages: any[]
}

export function BasicAgentChat() {
  const { state: agentState, setState: setAgentState } =
    useCoAgent<WeatherAgentState>({
      name: "basic_agent",
      initialState: { input: "New York City" }
    });

  const { appendMessage, isLoading } = useCopilotChat();

  // The form submit event should cover both hitting Enter and clicking Submit
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    appendMessage(
      new TextMessage({
        role: MessageRole.User,
        content: `
Please tell me the weather in the following location. If the input below is phrased as a question or is not recognizable as a location, and you can't make a reasonable guess as to what location I mean, ignore this prompt. The input is:

${agentState.input}
        `,
      })
    );
  }

  const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
    const input = e.target.value;
    setAgentState({
      ...agentState,
      input
    })
  }

  return (
    <div className='flex flex-col w-full max-w-lg border border-neutral-200 p-8 min-h-[50vh] '>
      <form onSubmit={handleSubmit} className='flex'>
        <input
          type="text"
          name="message_input"
          placeholder="Ask a question"
          value={agentState.input}
          onChange={handleChange}
          className='border border-r-0 border-neutral-300 p-2 flex-1'
        />
        <button type="submit" className='bg-neutral-600 text-white p-2 font-bold'>
          {isLoading ? "Working..." : "Submit"}
        </button>
      </form>
      <div className='flex-1'>
        {agentState && <div>{JSON.stringify(agentState, null, 1)}</div>}
      </div>
    </div>
  )
}