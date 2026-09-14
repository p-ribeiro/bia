import React from "react";
import DatePicker from "react-datepicker";
import { ptBR } from "date-fns/locale";
import "react-datepicker/dist/react-datepicker.css";
import { parseBRDate, formatBRDate } from "../utils/date";

// Campo de calendário reutilizável. Exibe e recebe a data sempre no formato
// dd/mm/yyyy (texto), mantendo o mesmo contrato de dados usado atualmente
// com o backend (campo dia_atividade é uma string livre).
//
// IMPORTANT: dd/mm/yyyy must be enforced UNCONDITIONALLY, regardless of the
// browser/OS locale (navigator.language, Intl defaults, etc.):
// - `dateFormat="dd/MM/yyyy"` pins the display order explicitly.
// - `locale={ptBR}` is passed explicitly (instead of leaving react-datepicker
//   to fall back to `getDefaultLocale()`) so the calendar never depends on a
//   locale registered/left unregistered elsewhere in the app.
// - `strictParsing` is required: react-datepicker's default parser
//   (`strictParsing: false`) silently falls back to the native `new Date(value)`
//   constructor whenever the primary dd/MM/yyyy parse fails to validate. That
//   native fallback assumes US month-first ordering (e.g. typing "09/14/2026"
//   gets silently accepted as month=09/day=14 instead of being rejected), which
//   is exactly the mm/dd/yyyy leak this fix addresses. Setting
//   `strictParsing={true}` disables that fallback so typed input is only ever
//   accepted when it matches dd/MM/yyyy exactly.
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
      locale={ptBR}
      strictParsing
      placeholderText={placeholder}
      className="date-picker-input"
      wrapperClassName="date-picker-wrapper"
      isClearable
      autoComplete="off"
    />
  );
};

export default DatePickerField;
