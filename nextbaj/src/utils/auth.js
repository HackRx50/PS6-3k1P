'use client'
import { useUser } from '@clerk/nextjs';

export const createUserInBackend = async () => {
  const { user } = useUser();

  if (user) {
    const userData = {
      fullname: user.fullName,
      email: user.primaryEmailAddress.emailAddress,
      is_admin: false
    };

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/create_user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error('Failed to create user in backend');
      }

      const result = await response.json();
      console.log('User created in backend:', result);
    } catch (error) {
      console.error('Error creating user in backend:', error);
    }
  }
};
