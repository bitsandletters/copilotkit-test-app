"use client";

import * as React from 'react'
import { useCoAgent, useCopilotChat } from "@copilotkit/react-core";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";
// import { CopilotPopup } from "@copilotkit/react-ui";

interface WeatherAgentState {
  final_response: {
    temperature: number;
    wind_direction: string;
    wind_speed: number;
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
  
  // const handleMessage = (content = '') => {
  //   appendMessage(
  //     new TextMessage({
  //       role: MessageRole.User,
  //       content,
  //     })
  //   );
  // };

  // The form submit event should cover both hitting Enter and clicking Submit
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // const formData = new FormData(e.target as HTMLFormElement);
    // const message = formData.get('message_input')

    // handleMessage(agentState.input);
    appendMessage(
      new TextMessage({
        role: MessageRole.User,
        content: agentState.input,
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

  // const messages = agentState.messages;
  console.log(agentState);

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
        {agentState.final_response && <div>{JSON.stringify(agentState.final_response, null, 1)}</div>}
      </div>
    </div>
  )
}