import React from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { parseBRDate, formatBRDate } from "../utils/date";

// Campo de calendário reutilizável. Exibe e recebe a data sempre no formato
// dd/mm/yyyy (texto), mantendo o mesmo contrato de dados usado atualmente
// com o backend (campo dia_atividade é uma string livre).
const DatePickerField = ({ id, value, onChange, placeholder = "dd/mm/aaaa" }) => {
  const selectedDate = parseBRDate(value);

  const handleChange = (date) => {
    onChange(date ? formatBRDate(date) : "");
  };

  return (
    <DatePicker
      id={id}
      selected={selectedDate}
      onChange={handleChange}
      dateFormat="dd/MM/yyyy"
      placeholderText={placeholder}
      className="date-picker-input"
      wrapperClassName="date-picker-wrapper"
      isClearable
      autoComplete="off"
    />
  );
};

export default DatePickerField;
