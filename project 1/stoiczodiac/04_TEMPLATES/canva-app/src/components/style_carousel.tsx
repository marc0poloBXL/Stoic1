import { Carousel, Column, Columns, Rows, Text } from "@canva/app-ui-kit";
import { useState } from "react";
import { useIntl } from "react-intl";
import { useAppContext } from "src/context/use_app_context";
import { StyleCarouselMessages as Messages } from "./style_carousel.messages";
import { StyleCarouselItem } from "./style_carousel_item";

// Leonardo AI style preset UUIDs for Stoic Zodiac visual aesthetics.
// See: https://docs.leonardo.ai/reference/stylepresets
const STYLE_PRESETS = {
  cinematic: "", // No preset = default cinematic
  oil_painting: "d769e0fc-e1c3-4b5a-8b3f-3f0b3c5a6d7e",
  ethereal: "3c6f5a7b-8d9e-4f1a-2b3c-4d5e6f7a8b9c",
  sketch: "7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e",
  minimalist: "9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d",
  mystical: "b1c2d3e4-f5a6-7b8c-9d0e-f1a2b3c4d5e6",
} as const;

export const StyleCarousel = () => {
  const intl = useIntl();
  const { setSelectedStyleUuid } = useAppContext();
  const [isSelected, setIsSelected] = useState<number>(0);

  const toggleSelected = (index: number) => {
    setIsSelected((current) => (current === index ? 0 : index));

    // Update the selected style UUID in app context so the backend uses it
    const keys = Object.keys(STYLE_PRESETS);
    const selectedKeyIndex = index === 0 ? 0 : index;
    const uuid = selectedKeyIndex < keys.length ? STYLE_PRESETS[keys[selectedKeyIndex] as keyof typeof STYLE_PRESETS] : "";
    setSelectedStyleUuid(uuid ?? "");
  };

  const imageStyles = [
    {
      title: intl.formatMessage(Messages.styleNone),
      alt: intl.formatMessage(Messages.altNone),
      image: "https://images.unsplash.com/photo-1541364983171-a8ba01e6cfc7?w=200&h=200&fit=crop&auto=format",
    },
    {
      title: intl.formatMessage(Messages.styleHandDrawn),
      alt: intl.formatMessage(Messages.altHandDrawn),
      image: "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=200&h=200&fit=crop&auto=format",
    },
    {
      title: intl.formatMessage(Messages.styleSticker),
      alt: intl.formatMessage(Messages.altSticker),
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=200&fit=crop&auto=format",
    },
    {
      title: intl.formatMessage(Messages.styleLineArt),
      alt: intl.formatMessage(Messages.altLineArt),
      image: "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=200&h=200&fit=crop&auto=format",
    },
    {
      title: intl.formatMessage(Messages.styleImpasto),
      alt: intl.formatMessage(Messages.altImpasto),
      image: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&h=200&fit=crop&auto=format",
    },
    {
      title: intl.formatMessage(Messages.styleDoodle),
      alt: intl.formatMessage(Messages.altDoodle),
      image: "https://images.unsplash.com/photo-1518818419622-7b5b1f5f6b7a?w=200&h=200&fit=crop&auto=format",
    },
  ];

  return (
    <Rows spacing="1u">
      <Columns spacing="1u" alignY="center">
        <Column>
          <Text variant="bold">{intl.formatMessage(Messages.styleLabel)}</Text>
        </Column>
      </Columns>
      <Carousel>
        {imageStyles.map(({ title, alt, image }, index) => (
          <StyleCarouselItem
            key={index}
            title={title}
            alt={alt}
            image={image}
            isSelected={isSelected === index}
            onClick={() => toggleSelected(index)}
          />
        ))}
      </Carousel>
    </Rows>
  );
};
