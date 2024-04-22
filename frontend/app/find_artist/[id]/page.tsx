// 'use client'
// import { useParams } from 'next/navigation'

// export default function FindArtists() {
//   const params = useParams()


//     return <div>This is the page to find information about {params.id}</div>
//   }

// 'use client'
// import { useEffect, useState } from 'react';
// import { useParams } from 'next/navigation'

// export default function FindArtists() {
//   const params = useParams()
//   const [artist, setArtist] = useState<string>('');

//   useEffect(() => {
//     if (params) {
//       fetch(`http://localhost:5000/find_artist/${params.id}`, {
//         mode: 'no-cors',
//         method: 'GET',
//         headers: {
//           'User-Agent': 'curl/7.88.1',
//           'Accept': '*/*'
//         }
//       })
//         .then(response => response.json())
//         .then(data => setArtist(data.artist))
//         .catch(error => console.error('Error fetching artist data:', error));
//     } else {
//       console.log("CHIGNADAMANDRE")
//     }
//   }, [params.id]);

//   // useEffect(() => {
//   //   if (params.id) {
//   //     fetch(`/api/proxy?id=${params.id}`)
//   //       .then(response => response.json())
//   //       .then(data => setArtist(data.artist))
//   //       .catch(error => console.error('Error fetching artist data:', error));
//   //   }
//   // }, [params.id]);

//   return (
//     <div>
//       This is the page to find information about {params.id}<br />
//       The predicted artist is: {artist}
//     </div>
//   );
// }



// 'use client' directive for automatic static optimization and client-side execution
'use client'
// Import necessary hooks and utilities from React and Next.js
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { useRouter } from 'next/navigation'
import { ChatBody, OpenAIModel } from '@/types/types';
import {
  Flex,
  Icon,
  useColorModeValue,
} from '@chakra-ui/react';
import { MdAutoAwesome, MdAutoAwesomeMotion, MdBolt, MdEdit, MdPerson } from 'react-icons/md';
import { Image, Heading, Text } from '@chakra-ui/react'
import { Spinner } from '@chakra-ui/react'

// Define the default export of the component for use in your Next.js application
export default function FindArtists() {
  // Retrieve dynamic route parameters using Next.js hook
  const params = useParams();
  // State hook for storing the artist data
  const [artist, setArtist] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [imageUrl, setImageUrl] = useState('');
  const router = useRouter();
  const [model, setModel] = useState<OpenAIModel>('gpt-4');
  const borderColor = useColorModeValue('gray.200', 'whiteAlpha.200');
  const inputColor = useColorModeValue('navy.700', 'white');
  const iconColor = useColorModeValue('brand.500', 'white');
  const bgIcon = useColorModeValue(
    'linear-gradient(180deg, #FBFBFF 0%, #CACAFF 100%)',
    'whiteAlpha.200',
  );
  const brandColor = useColorModeValue('brand.500', 'white');
  const buttonBg = useColorModeValue('white', 'whiteAlpha.100');
  const gray = useColorModeValue('gray.500', 'white');
  const buttonShadow = useColorModeValue(
    '14px 27px 45px rgba(112, 144, 176, 0.2)',
    'none',
  );
  const textColor = useColorModeValue('navy.700', 'white');
  const placeholderColor = useColorModeValue(
    { color: 'gray.500' },
    { color: 'whiteAlpha.600' },
  );



  // Effect hook for fetching artist data from the backend when the component mounts or params.id changes
  useEffect(() => {
    if (params.id) {
      setIsLoading(true);
      fetch(`http://localhost:8000/find_artist/${params.id}`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
          }
          return response.json();
        })
        // .then(data => setArtist(data.artist))
        // .catch(error => console.error('Error fetching artist data:', error));
        .then(data => {
          setArtist(data.artist);
          setImageUrl(`http://localhost:8000/images/${params.id}`);
          setIsLoading(false);
        })
        .catch(error => {
          console.error('Error fetching artist data:', error);
          setIsLoading(false);
        });
    }
  }, [params.id]);

  // Render the component with dynamic data
  // return (
  // <div>
  //   This is the page to find information about {params.id}<br />
  //   The predicted artist is: {artist}
  //   {isLoading ? (
  //       <p className="text-blue-500">Loading artist data...</p>
  //     ) : (
  //       <div className="mt-4">
  //         <p className="text-lg text-gray-700">
  //           <span className="font-semibold">Predicted Artist:</span> {artist || "Unknown"}
  //         </p>
  //       </div>
  //     )}
  // </div>
  // );

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        {/* <Heading as='h2' size='xl'>Artwork Information</Heading> */}

      <Flex
        mx="auto"
        zIndex="2"
        w="max-content"
        mb="20px"
        borderRadius="60px"
      >
        <Flex
          cursor={'pointer'}
          transition="0.3s"
          justify={'center'}
          align="center"
          bg={model === 'gpt-3.5-turbo' ? buttonBg : 'transparent'}
          w="174px"
          h="70px"
          boxShadow={model === 'gpt-3.5-turbo' ? buttonShadow : 'none'}
          borderRadius="14px"
          color={textColor}
          fontSize="18px"
          fontWeight={'700'}
          onClick={() => router.push(`/chat`)}
        >
          <Flex
            borderRadius="full"
            justify="center"
            align="center"
            bg={bgIcon}
            me="10px"
            h="39px"
            w="39px"
          >
            <Icon
              as={MdAutoAwesome}
              width="20px"
              height="20px"
              color={iconColor}
            />
          </Flex>
          Chat bot
        </Flex>
        {/* Second Option */}
        <Flex
          cursor={'pointer'}
          transition="0.3s"
          justify={'center'}
          align="center"
          bg={model === 'gpt-4' ? buttonBg : 'transparent'}
          w="164px"
          h="70px"
          boxShadow={model === 'gpt-4' ? buttonShadow : 'none'}
          borderRadius="14px"
          color={textColor}
          fontSize="18px"
          fontWeight={'700'}
          // onClick={() => setModel('gpt-4')}
          onClick={() => router.push(`/find_artist/${params.id}`)}
        >
          <Flex
            borderRadius="full"
            justify="center"
            align="center"
            bg={bgIcon}
            me="10px"
            h="39px"
            w="39px"
          >
            <Icon
              as={MdBolt}
              width="20px"
              height="20px"
              color={iconColor}
            />
          </Flex>
          Find Artist
        </Flex>

        {/* Third option */}
        <Flex
          cursor={'pointer'}
          transition="0.3s"
          justify={'center'}
          align="center"
          bg={model === 'gpt-5' ? buttonBg : 'transparent'}
          w="164px"
          h="70px"
          boxShadow={model === 'gpt-5' ? buttonShadow : 'none'}
          borderRadius="14px"
          color={textColor}
          fontSize="18px"
          fontWeight={'700'}
          // onClick={() => setModel('gpt-5')}
          onClick={() => router.push(`/make_animation/${params.id}`)}
        >
          <Flex
            borderRadius="full"
            justify="center"
            align="center"
            bg={bgIcon}
            me="10px"
            h="39px"
            w="39px"
          >
            <Icon
              as={MdAutoAwesomeMotion}
              width="20px"
              height="20px"
              color={iconColor}
            />
          </Flex>
          Animation
        </Flex>
      </Flex>



      <div>
      <Heading as='h2' size='xl'>Artwork Information</Heading>
      <Text fontSize='lg'> Information for artwork: {params.id}</Text>
        <p className="mt-2 text-gray-600">
          
        </p>
        {isLoading ? (
          <Spinner />
        ) : (
          <div className="mt-4">
            {/* Information */}
            <div >
              <Text fontSize='lg'> Predicted Artist: <Text as='b'>{artist}</Text> </Text>
              
              <Image boxSize='450px'
                objectFit='cover' src={imageUrl} alt="Uploaded Artwork" />
            </div>

          </div>
        )}
      </div>
    </div>
  );
}

