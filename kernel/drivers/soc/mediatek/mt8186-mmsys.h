/* SPDX-License-Identifier: GPL-2.0-only */

#ifndef __SOC_MEDIATEK_MT8186_MMSYS_H
#define __SOC_MEDIATEK_MT8186_MMSYS_H

#define MT8186_MMSYS_OVL_CON			0xF04
#define MT8186_MMSYS_OVL0_CON_MASK			0x3
#define MT8186_MMSYS_OVL0_2L_CON_MASK			0xC
#define MT8186_OVL0_GO_BLEND				BIT(0)
#define MT8186_OVL0_GO_BG				BIT(1)
#define MT8186_OVL0_2L_GO_BLEND				BIT(2)
#define MT8186_OVL0_2L_GO_BG				BIT(3)
#define MT8186_DISP_RDMA0_SOUT_SEL		0xF0C
#define MT8186_RDMA0_SOUT_SEL_MASK			0xF
#define MT8186_RDMA0_SOUT_TO_DSI0			(0)
#define MT8186_RDMA0_SOUT_TO_COLOR0			(1)
#define MT8186_RDMA0_SOUT_TO_DPI0			(2)
#define MT8186_DISP_OVL0_2L_MOUT_EN		0xF14
#define MT8186_OVL0_2L_MOUT_EN_MASK			0xF
#define MT8186_OVL0_2L_MOUT_TO_RDMA0			BIT(0)
#define MT8186_OVL0_2L_MOUT_TO_RDMA1			BIT(3)
#define MT8186_DISP_OVL0_MOUT_EN		0xF18
#define MT8186_OVL0_MOUT_EN_MASK			0xF
#define MT8186_OVL0_MOUT_TO_RDMA0			BIT(0)
#define MT8186_OVL0_MOUT_TO_RDMA1			BIT(3)
#define MT8186_DISP_DITHER0_MOUT_EN		0xF20
#define MT8186_DITHER0_MOUT_EN_MASK			0xF
#define MT8186_DITHER0_MOUT_TO_DSI0			BIT(0)
#define MT8186_DITHER0_MOUT_TO_RDMA1			BIT(2)
#define MT8186_DITHER0_MOUT_TO_DPI0			BIT(3)
#define MT8186_DISP_RDMA0_SEL_IN		0xF28
#define MT8186_RDMA0_SEL_IN_MASK			0xF
#define MT8186_RDMA0_FROM_OVL0				0
#define MT8186_RDMA0_FROM_OVL0_2L			2
#define MT8186_DISP_DSI0_SEL_IN			0xF30
#define MT8186_DSI0_SEL_IN_MASK				0xF
#define MT8186_DSI0_FROM_RDMA0				0
#define MT8186_DSI0_FROM_DITHER0			1
#define MT8186_DSI0_FROM_RDMA1				2
#define MT8186_DISP_RDMA1_MOUT_EN		0xF3C
#define MT8186_RDMA1_MOUT_EN_MASK			0xF
#define MT8186_RDMA1_MOUT_TO_DPI0_SEL			BIT(0)
#define MT8186_RDMA1_MOUT_TO_DSI0_SEL			BIT(2)
#define MT8186_DISP_RDMA1_SEL_IN		0xF40
#define MT8186_RDMA1_SEL_IN_MASK			0xF
#define MT8186_RDMA1_FROM_OVL0				0
#define MT8186_RDMA1_FROM_OVL0_2L			2
#define MT8186_RDMA1_FROM_DITHER0			3
#define MT8186_DISP_DPI0_SEL_IN			0xF44
#define MT8186_DPI0_SEL_IN_MASK				0xF
#define MT8186_DPI0_FROM_RDMA1				0
#define MT8186_DPI0_FROM_DITHER0			1
#define MT8186_DPI0_FROM_RDMA0				2

#define MT8186_MMSYS_SW0_RST_B				0x160

static const struct mtk_mmsys_routes mmsys_mt8186_routing_table[] = {
	{
		DDP_COMPONENT_OVL0, DDP_COMPONENT_RDMA0,
		MT8186_DISP_OVL0_MOUT_EN, MT8186_OVL0_MOUT_EN_MASK,
		MT8186_OVL0_MOUT_TO_RDMA0
	},
	{
		DDP_COMPONENT_OVL0, DDP_COMPONENT_RDMA0,
		MT8186_DISP_RDMA0_SEL_IN, MT8186_RDMA0_SEL_IN_MASK,
		MT8186_RDMA0_FROM_OVL0
	},
	{
		DDP_COMPONENT_OVL0, DDP_COMPONENT_RDMA0,
		MT8186_MMSYS_OVL_CON, MT8186_MMSYS_OVL0_CON_MASK,
		MT8186_OVL0_GO_BLEND
	},
	{
		DDP_COMPONENT_RDMA0, DDP_COMPONENT_COLOR0,
		MT8186_DISP_RDMA0_SOUT_SEL, MT8186_RDMA0_SOUT_SEL_MASK,
		MT8186_RDMA0_SOUT_TO_COLOR0
	},
	{
		DDP_COMPONENT_DITHER0, DDP_COMPONENT_DSI0,
		MT8186_DISP_DITHER0_MOUT_EN, MT8186_DITHER0_MOUT_EN_MASK,
		MT8186_DITHER0_MOUT_TO_DSI0,
	},
	{
		DDP_COMPONENT_DITHER0, DDP_COMPONENT_DSI0,
		MT8186_DISP_DSI0_SEL_IN, MT8186_DSI0_SEL_IN_MASK,
		MT8186_DSI0_FROM_DITHER0
	},
	{
		DDP_COMPONENT_OVL_2L0, DDP_COMPONENT_RDMA1,
		MT8186_DISP_OVL0_2L_MOUT_EN, MT8186_OVL0_2L_MOUT_EN_MASK,
		MT8186_OVL0_2L_MOUT_TO_RDMA1
	},
	{
		DDP_COMPONENT_OVL_2L0, DDP_COMPONENT_RDMA1,
		MT8186_DISP_RDMA1_SEL_IN, MT8186_RDMA1_SEL_IN_MASK,
		MT8186_RDMA1_FROM_OVL0_2L
	},
	{
		DDP_COMPONENT_OVL_2L0, DDP_COMPONENT_RDMA1,
		MT8186_MMSYS_OVL_CON, MT8186_MMSYS_OVL0_2L_CON_MASK,
		MT8186_OVL0_2L_GO_BLEND
	},
	{
		DDP_COMPONENT_RDMA1, DDP_COMPONENT_DPI0,
		MT8186_DISP_RDMA1_MOUT_EN, MT8186_RDMA1_MOUT_EN_MASK,
		MT8186_RDMA1_MOUT_TO_DPI0_SEL
	},
	{
		DDP_COMPONENT_RDMA1, DDP_COMPONENT_DPI0,
		MT8186_DISP_DPI0_SEL_IN, MT8186_DPI0_SEL_IN_MASK,
		MT8186_DPI0_FROM_RDMA1
	},
};

#endif /* __SOC_MEDIATEK_MT8186_MMSYS_H */