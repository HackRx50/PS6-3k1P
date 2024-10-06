import Image from "next/image";
import { useEffect, useState } from "react"

interface Card {
  Title: string;
  Script: string;
}

export default function ImageComp({ card, ind, processId }: { card: Card, ind: number, processId: string }) {

  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    console.log("Image component mounted")

    // get image from server for the prompt
    fetch(process.env.NEXT_PUBLIC_API_URL + '/generate_image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ script: card.Script, ind: ind, processId: processId }),
    })
      .then(response => response.json())
      .then(data => {

        console.log('Image data received:', data);
        setImageUrl(process.env.NEXT_PUBLIC_API_URL + '/get_image?filename=' + processId + '/' + ind + '.png');

      })
      .catch(error => {
        console.error('Error fetching image:', error);
      });

    // setImageUrl(process.env.NEXT_PUBLIC_API_URL + '/get_image?filename=' + processId + '/' + ind + '.png');

  }, [card.Script, ind, processId])

  return (
    <div
      // onClick={() => setSelectedCard(index)}
      className={`inline-block p-2 m-1 w-[300px] border rounded-lg cursor-pointer`}>
      {card.Title}
      {imageUrl && <Image src={imageUrl} alt="Fetched from server" height={300} width={300} />} {/* Display the image if available */}
    </div>
  )
}
