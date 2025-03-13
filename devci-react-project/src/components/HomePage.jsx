const HomePage = () => {
    return (
      <div 
        className="relative w-full min-h-screen bg-cover bg-center bg-no-repeat pt-16" 
        style={{ backgroundImage: "url('/assets/prescription.jpg')" }}
      >
        <div className="items-start max-w-5xl text-black p-45">
          <h2 className="text-3xl mt-6 font-bold">Here to provide your medicine solution!</h2>
          <p className=" text-1g mt-2 leading-relaxed p1-2  ">Prescription verification ensures your safety by confirming the accuracy of your medication, dosage, and potential drug interactions. 
            It helps prevent errors, allergies, and misuse while complying with medical and legal guidelines. 
            This process also protects against fraud and ensures you receive the right treatment. 
            Verifying prescriptions is essential for safe and effective healthcare.</p>
            <button type="submit"  className="bg-red-500
             hover:bg-red-600
             text-white px-4 py-2 rounded-lg t
             ransition duration-300 cursor-pointer">
                See Medicine Available</button>
        </div>
      </div>
    );
  };
  
  export default HomePage;
  