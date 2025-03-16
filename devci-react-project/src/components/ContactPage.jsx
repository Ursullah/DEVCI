import React from 'react'

const ContactPage = () => {
  return (
    <div>
      <h2>Contact us</h2>
      <form>
        <label>Your Name:</label>
        <input type='text' name='name' placeholder='Name'/>

        <label>Email Address:</label>
        <input type='text' name='email' placeholder='example@email.com'/>

        <label>Phone Number:</label>
        <input type='text' name='number' placeholder='O700000000'/>

        <textarea value={textarea}>Enter your message</textarea>

        <button type='submit'>Send</button>
      </form>
    </div>
  )
}

export default ContactPage
