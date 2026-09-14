// Utilitários para conversão de datas no formato brasileiro (dd/mm/yyyy)
// usado como formato de exibição e também como formato de texto enviado ao backend,
// mantendo compatibilidade com o valor já esperado pela API (campo dia_atividade é texto livre).

/**
 * Converte uma string no formato dd/mm/yyyy em um objeto Date.
 * Retorna null se a string estiver vazia ou não puder ser interpretada como uma data válida.
 */
export function parseBRDate(value) {
  if (!value || typeof value !== "string") return null;

  const match = value.trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!match) return null;

  const day = Number(match[1]);
  const month = Number(match[2]);
  const year = Number(match[3]);

  const date = new Date(year, month - 1, day);

  // Garante que a data é válida (ex.: rejeita 31/02/2026)
  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return null;
  }

  return date;
}

/**
 * Formata um objeto Date como string dd/mm/yyyy.
 * Retorna string vazia caso a data seja inválida/nula.
 */
export function formatBRDate(date) {
  if (!(date instanceof Date) || isNaN(date.getTime())) return "";

  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}
