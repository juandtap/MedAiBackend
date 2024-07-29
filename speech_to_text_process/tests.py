# Importar la biblioteca

# Configurar la clave de API de OpenAI
#openai.api_key = 'sk-None-pZvhT36Lo37E34AZP0ZZT3BlbkFJm5LRgULNtRF4ufYykAXu'
url = 'https://api.openai.com/v1/chat/completions'
# El texto proporcionado
texto = """
Buenos días, señor González. ¿Cómo se encuentra hoy?
Buenos días, doctor. Me siento un poco mejor, gracias. ¿Qué necesitamos revisar hoy?
Vamos a completar algunos datos para actualizar su expediente. ¿Puede decirme su nombre completo?
Claro, mi nombre es Juan Carlos González.
Perfecto, Juan Carlos. ¿Cuál es su ID de paciente?
Mi ID es 987654.
¿Y cuántos años tiene, Juan Carlos?
Tengo 45 años.
Entendido. ¿Cuál es su género?
Soy masculino.
Muy bien. ¿Me puede proporcionar su dirección actual?
Sí, vivo en la Calle Falsa 123, Ciudad Ficticia.
Gracias. ¿Y su número de celular?
Mi número de celular es 123-456-7890.
Perfecto. ¿Podría darme su correo electrónico?
Claro, es juancarlos.gonzalez@example.com.
Gracias. Ahora, respecto a su diagnóstico, ¿podría describirme brevemente sus síntomas y el diagnóstico actual?
He tenido dolores de cabeza constantes y náuseas. El diagnóstico actual es migraña crónica.
Entendido. ¿Tiene alguna alergia que debamos tener en cuenta?
Sí, soy alérgico a la penicilina.
Muy bien, Juan Carlos. Hemos completado toda la información necesaria. ¿Hay algo más que quiera agregar?
No, eso sería todo, doctor. Muchas gracias.
De nada, Juan Carlos. Cuídese mucho y estamos en contacto para cualquier cosa que necesite.
"""
#
# # Crear la solicitud a la API de OpenAI
# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role","user"},
#     {"content": f"Eres un asistente que extrae datos personales de los diálogos. Extrae los datos personales del siguiente texto:\n\n{texto}"}
#   ],
#   max_tokens = 150
# )
#
# # Mostrar la respuesta
# print(response.choices[0].message['content'].strip())