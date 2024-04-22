'use client'

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Flex, Heading, Icon, Spinner, useColorModeValue } from '@chakra-ui/react';
import { ChatBody, OpenAIModel } from '@/types/types';
import { MdAutoAwesome, MdAutoAwesomeMotion, MdBolt, MdEdit, MdPerson } from 'react-icons/md';
import { useRouter } from 'next/navigation'

export default function Animation() {
    const params = useParams();
    const router = useRouter();
    const [videoUrl, setVideoUrl] = useState('');
    const [loading, setLoading] = useState(true);

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

    useEffect(() => {

        const fetchVideo = async (generationId: String) => {
            const url = `https://api.stability.ai/v2beta/image-to-video/result/${generationId}`;
            const headers = {
                'accept': "video/*",
                'authorization': `Bearer ${process.env.NEXT_PUBLIC_STABILITY_API_KEY}`
            };

            // Try to fetch the video. Retry if the response status is 202 (Accepted)
            let response = await fetch(url, { headers });
            while (response.status === 202) {
                await new Promise(resolve => setTimeout(resolve, 5000));
                response = await fetch(url, { headers });
            }

            if (response.ok) {
                const blob = await response.blob();
                setVideoUrl(URL.createObjectURL(blob));
                setLoading(false);
            } else {
                console.error('Failed to load video from Stability AI');
                setLoading(false);
            }
        };

        const fetchGenerationId = async () => {
            if (params.id) {
                try {
                    const response = await fetch(`http://localhost:8000/make_animation/${params.id}`);
                    const data = await response.json();
                    if (data.generation_ID) {
                        console.log(`Generation id obtained: ${data.generation_ID}`)
                        await fetchVideo(data.generation_ID);
                    } else {
                        setLoading(false);
                        console.error('No generation ID received');
                    }
                } catch (error) {
                    setLoading(false);
                    console.error('Error fetching generation ID:', error);
                }
            }
        };

        fetchGenerationId();
    }, [params.id]);

    if (loading) return <div >
        Generating video...
        <Spinner />
    </div>;
    return (
        <div>
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



            <Heading as='h3' size='lg'>
                Watch the animation!
            </Heading>
            {videoUrl && <video src={videoUrl} controls autoPlay loop />}
        </div>
    );
}
