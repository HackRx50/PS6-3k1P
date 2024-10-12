import Loader from "@/components/Loader";
import Image from "next/image";
import { useEffect, useState } from "react";

interface Card {
  Title: string
  Script: string
}

export default function ImageComp({ card, ind, processId, height, width }: { card: Card; ind: number; processId: string; height: number; width: number }) {
  const [imageUrl, setImageUrl] = useState<string | null>(null)

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/generate_image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ script: card.Script, ind: ind, processId: processId, height: height, width: width }),
    })
      .then(response => response.json())
      .then(data => {
        setImageUrl(process.env.NEXT_PUBLIC_API_URL + "/get_image?filename=" + processId + "/" + ind + ".png")
      })
      .catch(error => {
        console.error("Error fetching image:", error)
      })

    // setImageUrl(process.env.NEXT_PUBLIC_API_URL + '/get_image?filename=' + processId + '/' + ind + '.png');
  }, [card.Script, ind, processId])

  return (
    <div
      // onClick={() => setSelectedCard(index)}
      className={`inline-block p-2 m-1 w-[300px] border rounded-lg cursor-pointer`}>
      {card.Title}
      {
        imageUrl ? (
          <Image src={imageUrl} alt="Fetched from server" height={300} width={300} />
        ) : (
          <Loader />
          // <span>
          //   Loading ...
          // </span>
        )
      }
    </div>
  )
}
