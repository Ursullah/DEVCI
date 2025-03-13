import { useState } from "react";

const RoleDropdown = ({onSelectRole}) =>{
    const[isOpen, setIsOpen] = useState(false);
    const[selectedRole, setSelectedRole] = useState("Select Role")

    const roles = ["Doctor", "Pharmacist", "Patient", "Admin"];

    const handleRoleSelect = (role) =>{
        setSelectedRole(role);
        setIsOpen(false);
        onSelectRole(role)
    };
    
    return(
        <div>
            <button onClick={() =>setIsOpen(!isOpen)}>
               {selectedRole}
            </button>
            {isOpen && (
                <div>
                    <ul> {role.map((role) =>(
                        <li key={role}>
                            <button
                            onClick={() => handleSelect(role)}>

                            </button>
                        </li>
                    ))}

                    </ul>
                </div>
            )}
        </div>
    )
}
export default RoleDropdown;