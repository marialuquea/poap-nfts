import streamlit as st
from web3 import Web3
import openai
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.text import MIMEText

# OpenAI setup
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

# Web3 setup
infura_url = 'YOUR_INFURA_PROJECT_URL'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = 'YOUR_CONTRACT_ADDRESS'
abi = 'YOUR_CONTRACT_ABI'
contract = web3.eth.contract(address=contract_address, abi=abi)

def mint_nft(image_url, recipient_address):
    nonce = web3.eth.getTransactionCount('YOUR_WALLET_ADDRESS')
    txn = contract.functions.mintNFT(
        recipient_address, image_url
    ).buildTransaction({
        'chainId': 1,
        'gas': 70000,
        'gasPrice': web3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3.eth.account.signTransaction(txn, private_key='YOUR_PRIVATE_KEY')
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(tx_hash)

# Email setup
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your-email@example.com'
smtp_password = 'your-email-password'

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())

# Streamlit app
def main():
    st.title("Event NFT Generator")

    st.header("Event Organizer Sign In")
    organizer_name = st.text_input("Organizer Name")
    organizer_email = st.text_input("Organizer Email")

    st.header("Write NFT Description")
    nft_description = st.text_area("Description")

    unique_collection = st.checkbox("Unique Collection per event?")

    if st.button("Create Collection"):
        collection_id = f"collection_{organizer_name.replace(' ', '_')}"
        st.session_state['collection_id'] = collection_id
        st.success("Collection created successfully!")
        st.write(f"Collection ID: {collection_id}")

    st.header("Attendee Joins Event")
    attendee_name = st.text_input("Attendee Name")
    attendee_email = st.text_input("Attendee Email")
    attendee_wallet = st.text_input("Attendee ETH Wallet")

    if st.button("Join Event"):
        if 'collection_id' not in st.session_state:
            st.error("Please create a collection first.")
            return

        collection_id = st.session_state['collection_id']
        
        if attendee_wallet:
            if Web3.isAddress(attendee_wallet):
                try:
                    # Generate Image
                    image_url = generate_image(nft_description)
                    # Mint NFT
                    tx_hash = mint_nft(image_url, attendee_wallet)
                    st.success(f"NFT Minted! Transaction Hash: {tx_hash}")
                except Exception as e:
                    st.error(f"Error minting NFT: {e}")
            else:
                st.error("Invalid Ethereum address")
        else:
            try:
                validate_email(attendee_email)
                send_email(attendee_email, "Create your Ethereum Wallet", "Please create an Ethereum wallet to receive your NFT.")
                st.success("Email sent to attendee to create an Ethereum wallet.")
            except EmailNotValidError as e:
                st.error(f"Invalid email address: {e}")

if __name__ == "__main__":
    main()
