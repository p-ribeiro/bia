import React from "react";
import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "./ui/chart";

// A "prioridade" da tarefa hoje é representada pelo campo booleano `importante`.
// Definimos os dois níveis de prioridade existentes para agrupar as tarefas.
const PRIORITY_LEVELS = [
  {
    key: "importante",
    label: "Importante",
    match: (task) => !!task.importante,
  },
  {
    key: "normal",
    label: "Normal",
    match: (task) => !task.importante,
  },
];

const chartConfig = {
  count: {
    label: "Tarefas",
  },
  importante: {
    label: "Importante",
    color: "var(--chart-1)",
  },
  normal: {
    label: "Normal",
    color: "var(--chart-2)",
  },
};

const TasksByPriority = ({ tasks = [] }) => {
  const hasTasks = tasks.length > 0;

  const chartData = PRIORITY_LEVELS.map(({ key, match }) => ({
    priority: key,
    count: tasks.filter(match).length,
    fill: `var(--color-${key})`,
  }));

  return (
    <div className="tasks-by-priority-page">
      <Card>
        <CardHeader>
          <CardTitle>Tarefas por Prioridade</CardTitle>
          <CardDescription>
            Quantidade de tarefas agrupadas por nível de prioridade
          </CardDescription>
        </CardHeader>
        <CardContent>
          {hasTasks ? (
            <ChartContainer config={chartConfig} className="min-h-[220px] w-full">
              <BarChart
                accessibilityLayer
                data={chartData}
                layout="vertical"
                margin={{ left: 12 }}
              >
                <CartesianGrid horizontal={false} />
                <YAxis
                  dataKey="priority"
                  type="category"
                  tickLine={false}
                  tickMargin={10}
                  axisLine={false}
                  tickFormatter={(value) => chartConfig[value]?.label ?? value}
                />
                <XAxis dataKey="count" type="number" allowDecimals={false} hide />
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent hideLabel nameKey="priority" />}
                />
                <Bar dataKey="count" radius={5} />
              </BarChart>
            </ChartContainer>
          ) : (
            <div className="empty-state">
              <h3>Nenhuma tarefa por aqui 📝</h3>
              <p>Adicione tarefas na tela principal para ver o gráfico de prioridades.</p>
            </div>
          )}
        </CardContent>
      </Card>

      <div className="about-footer">
        <Link to="/" className="back-button">
          ← Voltar para Tarefas
        </Link>
      </div>
    </div>
  );
};

export default TasksByPriority;
