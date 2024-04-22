'use client';
/*eslint-disable*/

import Link from '@/components/link/Link';
import MessageBoxChat from '@/components/MessageBox';
import { ChatBody, OpenAIModel } from '@/types/types';
import {
    Accordion,
    AccordionButton,
    AccordionIcon,
    AccordionItem,
    AccordionPanel,
    Box,
    Button,
    Flex,
    Icon,
    Img,
    Input,
    Text,
    HStack,
    useColorModeValue,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { MdAutoAwesome, MdAutoAwesomeMotion, MdBolt, MdEdit, MdPerson } from 'react-icons/md';
// import Bg from '../public/img/chat/logo_faded.png';
import { useRouter } from 'next/navigation'
import OpenAI from 'openai';
import { UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { message, Upload } from 'antd';

export default function Chat(props: { apiKeyApp: string }) {
    const router = useRouter();
    // Input States
    const [inputOnSubmit, setInputOnSubmit] = useState<string>('');
    const [inputCode, setInputCode] = useState<string>('');
    // Response message
    const [outputCode, setOutputCode] = useState<string | null>(' ');
    // ChatGPT model
    const [model, setModel] = useState<OpenAIModel>('gpt-3.5-turbo');
    // Loading state
    const [loading, setLoading] = useState<boolean>(false);
    // File name
    const [artFileName, setArtFileName] = useState<string>('');

    //   TODO: get server art work
    const [artPiece, setArtPiece] = useState('art');
    const [chatMessages, setChatMessages] = useState<Array<any>>([
        {
            role: "system", content: `You are a helpful art assistant that knows everything about ${artPiece}`
        },
    ]);

    useEffect(() => {
        const fetchArtwork = async () => {
            
            try {
                const response = await fetch('http://localhost:8000/chat_artwork', {
                    credentials: 'include'
                });
                const data = await response.json();
                if (response.ok) {
                    setArtPiece(data.artwork);
                    console.log(data.artwork)
                    setChatMessages([
                        {
                            role: "system", content: `You are a helpful art assistant that knows everything about ${data.artwork}`
                        },
                    ])
                } else {
                    throw new Error('Failed to fetch artwork info');
                }
            } catch (error) {
                console.error('Error fetching artwork info:', error);
                setArtPiece('Failed to load artwork info');
            }
        };

        fetchArtwork();
    }, []); 

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

    // Update chatMessages state
    const addMessageToChat = (newMessage: { role: string /*eslint-disable*/; content: string | null; }) => {
        setChatMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    // OPENAI API LOGIC
    const openai = new OpenAI({
        apiKey: process.env['NEXT_PUBLIC_OPENAI_API_KEY'],
        dangerouslyAllowBrowser: true
    });

    const getResponse = async (message: string) => {
        const newMessage = { role: 'user', content: message }
        // setChatMessages([...chatMessages, newMessage]); 
        const updatedChatMessages = [...chatMessages, newMessage];
        setChatMessages(updatedChatMessages);

        console.log(updatedChatMessages)
        // setChatMessages( chatMessages.push(newMessage) ) // No sirve

        const response = await openai.chat.completions.create({
            messages: updatedChatMessages,
            model: "gpt-3.5-turbo",
        });

        var current_response = response ? response.choices[0].message.content : ' ';
        addMessageToChat({ role: 'assistant', content: current_response });
        return current_response;
    };

    // getResponse();




    const handleTranslate = async () => {
        // let apiKey = localStorage.getItem('apiKey');
        // Chat post conditions(maximum number of characters, valid message etc.)
        const maxCodeLength = model === 'gpt-3.5-turbo' ? 700 : 700;

        if (!inputCode) {
            alert('Please enter your message.');
            return;
        }

        if (inputCode.length > maxCodeLength) {
            alert(
                `Please enter code less than ${maxCodeLength} characters. You are currently at ${inputCode.length} characters.`,
            );
            return;
        }
        setOutputCode(' ');
        setLoading(true);
        setInputCode('');
        setInputOnSubmit(inputCode);
        setOutputCode(await getResponse(inputCode));
        setInputCode('')
        setLoading(false);
    };


    const handleChange = (Event: any) => {
        setInputCode(Event.target.value);
    };

    return (
        <Flex
            w="100%"
            pt={{ base: '70px', md: '0px' }}
            direction="column"
            position="relative"
        >
            <Flex
                direction="column"
                mx="auto"
                w={{ base: '100%', md: '100%', xl: '100%' }}
                minH={{ base: '75vh', '2xl': '85vh' }}
                maxW="1000px"
            >
                {/* Model Change */}
                <Flex direction={'column'} w="100%" mb={outputCode ? '20px' : 'auto'}>
                    {/* TOOD: Display options and routing */}
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
                            onClick={() => setModel('gpt-3.5-turbo')}
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
                            onClick={() => router.push('/find_artist')}
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
                            onClick={() => router.push('/make_animation')}
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

                </Flex>
                {/* Main Box */}
                <Flex
                    direction="column"
                    w="100%"
                    mx="auto"
                    //   display={outputCode ? 'flex' : 'none'}
                    mb={'auto'}
                >
                    <Flex w="100%" align={'center'} mb="10px">
                        <Flex
                            borderRadius="full"
                            justify="center"
                            align="center"
                            bg={'transparent'}
                            border="1px solid"
                            borderColor={borderColor}
                            me="20px"
                            h="40px"
                            minH="40px"
                            minW="40px"
                        >
                            <Icon
                                as={MdPerson}
                                width="20px"
                                height="20px"
                                color={brandColor}
                            />
                        </Flex>
                        <Flex
                            p="22px"
                            border="1px solid"
                            borderColor={borderColor}
                            borderRadius="14px"
                            w="100%"
                            zIndex={'2'}
                        >
                            <Text
                                color={textColor}
                                fontWeight="600"
                                fontSize={{ base: 'sm', md: 'md' }}
                                lineHeight={{ base: '24px', md: '26px' }}
                            >
                                {inputOnSubmit}
                            </Text>
                            <Icon
                                cursor="pointer"
                                as={MdEdit}
                                ms="auto"
                                width="20px"
                                height="20px"
                                color={gray}
                            />
                        </Flex>
                    </Flex>
                    <Flex w="100%">
                        <Flex
                            borderRadius="full"
                            justify="center"
                            align="center"
                            bg={'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)'}
                            me="20px"
                            h="40px"
                            minH="40px"
                            minW="40px"
                        >
                            <Icon
                                as={MdAutoAwesome}
                                width="20px"
                                height="20px"
                                color="white"
                            />
                        </Flex>
                        <MessageBoxChat output={outputCode} />
                    </Flex>
                </Flex>
                {/* Chat Input */}
                <Flex
                    ms={{ base: '0px', xl: '60px' }}
                    mt="20px"
                    justifySelf={'flex-end'}
                >

                    {/* Chat text field input */}
                    <Input
                        minH="54px"
                        h="100%"
                        border="1px solid"
                        borderColor={borderColor}
                        borderRadius="45px"
                        p="15px 20px"
                        me="10px"
                        fontSize="sm"
                        fontWeight="500"
                        _focus={{ borderColor: 'none' }}
                        color={inputColor}
                        _placeholder={placeholderColor}
                        placeholder="Type your message here..."
                        onChange={handleChange}
                    // display={outputCode ? "" : "none"}
                    />

                    {/* Submit button */}
                    <Button
                        variant="primary"
                        py="20px"
                        px="16px"
                        fontSize="sm"
                        borderRadius="45px"
                        ms="auto"
                        w={{ base: '160px', md: '210px' }}
                        h="54px"
                        _hover={{
                            boxShadow:
                                '0px 21px 27px -10px rgba(96, 60, 255, 0.48) !important',
                            bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%) !important',
                            _disabled: {
                                bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)',
                            },
                        }}
                        onClick={handleTranslate}
                        isLoading={loading ? true : false}
                    >
                        Submit
                    </Button>
                </Flex>

                <Flex
                    justify="center"
                    mt="20px"
                    direction={{ base: 'column', md: 'row' }}
                    alignItems="center"
                >
                    <Text fontSize="xs" textAlign="center" color={gray}>
                        Running latest version of ArtEcho.
                    </Text>
                    <Link href="">
                        <Text
                            fontSize="xs"
                            color={textColor}
                            fontWeight="500"
                            textDecoration="underline"
                        >
                            Built with ❤️ for professor Austin
                        </Text>
                    </Link>
                </Flex>
            </Flex>
        </Flex>
    );
}
