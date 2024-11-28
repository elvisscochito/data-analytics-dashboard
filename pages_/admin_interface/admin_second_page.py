import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests

# define the function to the second page of the admin interface and be called in the main file
def admin_second_page():
	# sidebar icon
	st.logo(
		"danu.png",
		icon_image="logo_copy.png",
		size="large"
	)

	if st.sidebar.button("Logout", key="admin_logout_button_2"):
		st.session_state.authenticated = False
		st.success("Logout successful")

	st.title("Chatbot")

	# Chatbot integration
	st.components.v1.html("""
		<script> window.chtlConfig = { chatbotId: "1174567888", display: "fullscreen" } </script>
		<script async data-id="1174567888" id="chatling-embed-script" data-display="fullscreen" type="text/javascript" src="https://chatling.ai/js/embed.js"></script>
	""", height=400)

	""" # init messages history
	if "messages" not in st.session_state:
		st.session_state.messages = []

	# define the function to send a message
	def send_message(message):
		st.session_state.messages.append({"role": "user", "message": message})

	# define the function to receive a message
	def receive_message(message):
		st.session_state.messages.append({"role": "assistant", "message": message})

	# define the function to display the messages
	def display_messages():
		for message in st.session_state.messages:
			if message["role"] == "user":
				with st.chat_message(name="user", avatar="👤"):
					st.write(message["message"])
			else:
				with st.chat_message(name="assistant", avatar="🤖"):
					# with st.spinner("Chatbot is typing..."):
					st.write(message["message"])

	# define the function to handle the chatbot
	def chatbot():
		# get the user input
		if prompt := st.chat_input("User input"):
			# send the user input
			send_message(prompt)

			# receive the chatbot response
			receive_message("Chatbot response")
		display_messages()

	# call the chatbot function
	chatbot() """

	""" if prompt := st.chat_input("User input"):
		with st.chat_message(name="user", avatar="👤"):
			st.write(prompt)

		# add user message to history
		st.session_state.messages.append({"role": "user", "message": prompt})

		# chatbot response
		with st.chat_message(name="assistant", avatar="🤖"):
			with st.spinner("Chatbot is typing..."):
				st.write("Chatbot response")

		# add chatbot response to history
		st.session_state.messages.append({"role": "assistant", "message": "Chatbot response"}) """

	""" with st.chat_message(name="assistant", avatar="🤖"):
		st.write("Chatbot response")

	with st.chat_message(name="user", avatar="👤"):
		st.write("User input") """

	""" with st.form("chatbot_form"):
		user_input = st.text_input("User input")
		st.form_submit_button("Send") """
