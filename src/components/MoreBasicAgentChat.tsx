"use client";

import { useCoAgentAction } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

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

export function MoreBasicAgentChat() {
  useCoAgentAction<WeatherAgentState>({
    name: "basic_agent",
    nodeName: "respond",
    render: ({ status, state, nodeName }) => {
      return `
Conditions: ${state.final_response.conditions}, Temperature: ${state.final_response.temperature}ºF
`
    },
    handler: ({ state, nodeName }) => {
      console.log("handler", { state, nodeName });
      // ...
    },
  })

  return (
    <CopilotChat
      labels={{
        title: "Weather Assistant",
        initial: "Where would you like to go?",
      }}
    />
  )
}