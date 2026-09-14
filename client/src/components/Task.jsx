import React, { useState } from "react";
import { FaTimes, FaStar, FaRegStar, FaEdit, FaCheck, FaBan } from "react-icons/fa";
import DatePickerField from "./DatePickerField";

const Task = ({ task, onDelete, onToggle, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [titulo, setTitulo] = useState(task.titulo);
  const [dia, setDia] = useState(task.dia_atividade || "");

  const startEditing = () => {
    setTitulo(task.titulo);
    setDia(task.dia_atividade || "");
    setIsEditing(true);
  };

  const cancelEditing = () => {
    setIsEditing(false);
  };

  const saveEditing = () => {
    if (!titulo.trim()) return;

    onUpdate(task.uuid, {
      titulo: titulo.trim(),
      dia_atividade: dia,
    });
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className={`task task-editing ${task.importante ? "reminder" : ""}`}>
        <div className="task-content">
          <input
            type="text"
            className="task-edit-title"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            autoFocus
          />
          <div className="task-edit-date">
            <DatePickerField value={dia} onChange={setDia} />
          </div>
        </div>
        <div className="task-actions">
          <button className="task-save" onClick={saveEditing} title="Salvar">
            <FaCheck />
          </button>
          <button className="task-cancel" onClick={cancelEditing} title="Cancelar">
            <FaBan />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`task ${task.importante ? "reminder" : ""}`}
      onDoubleClick={() => onToggle(task.uuid)}
    >
      <div className="task-content">
        <h3>{task.titulo}</h3>
        <p className="task-date">
          📅 {task.dia_atividade || "Sem data definida"}
        </p>
      </div>
      <div className="task-actions">
        <button
          className="task-priority"
          onClick={() => onToggle(task.uuid)}
          title={task.importante ? "Remover importante" : "Marcar importante"}
        >
          {task.importante ? <FaStar /> : <FaRegStar />}
        </button>
        <button
          className="task-edit"
          onClick={startEditing}
          title="Editar"
        >
          <FaEdit />
        </button>
        <button
          className="task-delete"
          onClick={() => onDelete(task.uuid)}
          title="Excluir"
        >
          <FaTimes />
        </button>
      </div>
    </div>
  );
};

export default Task;
