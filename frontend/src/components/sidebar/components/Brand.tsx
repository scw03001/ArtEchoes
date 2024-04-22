'use client';
// Chakra imports
import { Box, Flex, useColorModeValue } from '@chakra-ui/react';

import { HorizonLogo } from '@/components/icons/Icons';
import { Image } from '@chakra-ui/react'
import { HSeparator } from '@/components/separator/Separator';
import { useRouter } from 'next/navigation'

export function SidebarBrand() {
  //   Chakra color mode
  let logoColor = useColorModeValue('navy.700', 'white');

  const router = useRouter();

  return (
    <Flex alignItems="center" flexDirection="column">
      <button>
        <HorizonLogo h="70px" w="146px" my="30px" color={logoColor} onClick={() => router.replace('/')}
         />
      </button>
        
      {/* <Box boxSize='sm'>
        <Image src='logos/ArtEcho.svg' alt='ArtEcho' />
      </Box> */}
      <HSeparator mb="20px" w="284px" />
    </Flex>
  );
}

export default SidebarBrand;
